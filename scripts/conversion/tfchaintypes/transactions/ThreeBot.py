from .Base import TransactionBaseClass, TransactionVersion, InputSignatureHashFactory

from ..FulfillmentTypes import ED25519Signature, SignatureCallbackBase, SignatureRequest
from ..ConditionTypes import ConditionBaseClass, ConditionNil
from ..ThreeBot import NetworkAddress, BotName
from ..PrimitiveTypes import BinaryData, Currency
from ..CryptoTypes import PublicKey
from ..IO import CoinInput, CoinOutput

from abc import abstractmethod


class BotTransactionBaseClass(TransactionBaseClass, SignatureCallbackBase):
    BOT_FEE_NETWORK_ADDRESS_UPDATE = Currency(value="20 TFT")
    BOT_FEE_ADDITIONAL_NAME = Currency(value="50 TFT")
    BOT_FEE_REGISTRATION = Currency(value="90 TFT")
    BOT_FEE_MONTHLY = Currency(value="10 TFT")

    MAX_NAMES_PER_BOT = 5
    MAX_ADDRESSES_PER_BOT = 10

    SPECIFIER_SENDER = BinaryData(value=b"sender", fixed_size=0)
    SPECIFIER_RECEIVER = BinaryData(value=b"receiver", fixed_size=0)

    @staticmethod
    def compute_monthly_bot_fees(months):
        """
        computes the total monthly fees required for the given months,
        using the given oneCoin value as the currency's unit value.
        """
        fees = BotTransactionBaseClass.BOT_FEE_MONTHLY * months
        if months < 12:
            return fees
        if months < 24:
            return fees * 0.7
        return fees * 0.5

    @property
    @abstractmethod
    def required_bot_fees(self):
        """
        The bot fees required to pay for this Bot Transaction.
        """
        pass


class BotMonthsAndFlagsData(j.data.rivine.BaseSiaObjectEncoder, j.data.rivine.BaseRivineObjectEncoder):
    def __init__(self, number_of_months, has_addresses, has_names, has_refund):
        if not isinstance(number_of_months, int) or number_of_months < 0 or number_of_months > 24:
            raise j.exceptions.Value(
                "{} ({}) is not a valid number of months, has to be a integer in the [0,24] range".format(
                    number_of_months, type(number_of_months)
                )
            )
        self._number_of_months = number_of_months
        if not isinstance(has_addresses, bool):
            raise j.exceptions.Value("has_addresses has to be a bool, not {}".format(type(has_addresses)))
        self._has_addresses = has_addresses
        if not isinstance(has_names, bool):
            raise j.exceptions.Value("has_names has to be a bool, not {}".format(type(has_names)))
        self._has_names = has_names
        if not isinstance(has_refund, bool):
            raise j.exceptions.Value("has_refund has to be a bool, not {}".format(type(has_refund)))
        self._has_refund = has_refund

    @property
    def number_of_months(self):
        return self._number_of_months

    @property
    def has_addresses(self):
        return self._has_addresses

    @property
    def has_names(self):
        return self._has_names

    @property
    def has_refund(self):
        return self._has_refund

    def sia_binary_encode(self, encoder):
        """
        Sia binary encodes a BotMonthsAndFlagsData as a one-byte flag,
        uses the Rivine Encoder. See rivine_binary_encode for more information.
        """
        e = j.data.rivine.encoder_rivine_get()
        self.rivine_binary_encode(e)
        encoder.add_array(e.data)

    def rivine_binary_encode(self, encoder):
        """
        Rivine binary encodes a BotMonthsAndFlagsData as a one-byte flag.
        """
        flag = self._number_of_months
        if self._has_addresses:
            flag |= 32
        if self._has_names:
            flag |= 64
        if self._has_refund:
            flag |= 128
        encoder.add_int8(flag)


class TransactionV144(BotTransactionBaseClass):
    _SPECIFIER = b"bot register tx\0"

    def __init__(self):
        self._addresses = []
        self._names = []
        self._number_of_months = 0
        self._transaction_fee = None
        self._coin_inputs = []
        self._refund_coin_output = None
        self._public_key = None
        self._signature = None

        super().__init__()

    @property
    def version(self):
        return TransactionVersion.THREEBOT_REGISTRATION

    @property
    def required_bot_fees(self):
        """
        The fees required to pay for this 3Bot Registration Transaction.
        """
        # a static registration fee has to be paid
        fees = 0 + BotTransactionBaseClass.BOT_FEE_REGISTRATION
        # the amount of desired months also has to be paid
        fees += BotTransactionBaseClass.compute_monthly_bot_fees(self._number_of_months)
        # if more than one name is defined it also has to be paid
        lnames = len(self._names)
        if lnames > 1:
            fees += BotTransactionBaseClass.BOT_FEE_ADDITIONAL_NAME * (lnames - 1)
        # no fee has to be paid for the used network addresses during registration
        # return the total fees
        return fees

    @property
    def coin_inputs(self):
        """
        Coin inputs of this Transaction,
        used as funding for coin outputs, fees and any other kind of coin output.
        """
        return self._coin_inputs

    @coin_inputs.setter
    def coin_inputs(self, value):
        self._coin_inputs = []
        if not value:
            return
        for ci in value:
            self.coin_input_add(ci.parentid, ci.fulfillment, parent_output=ci.parent_output)

    @property
    def refund_coin_output(self):
        if self._refund_coin_output is None:
            return CoinOutput()
        return self._refund_coin_output

    @property
    def coin_outputs(self):
        """
        Empty list, or a singleton with the refund coin output if that one exists.
        """
        if self._refund_coin_output is None:
            return []
        return [self._refund_coin_output]

    @coin_outputs.setter
    def coin_outputs(self, value):
        if isinstance(value, list):
            lvalue = len(value)
            if lvalue == 0:
                value = None
            elif lvalue == 1:
                value = value[0]
            else:
                raise j.exceptions.Value("ThreeBot only can have one coin output, a refund coin output")
        if value is None:
            self._refund_coin_output = None
        elif isinstance(value, CoinOutput):
            self._refund_coin_output = CoinOutput(value=value.value, condition=value.condition)
            self._refund_coin_output.id = value.id
        else:
            raise j.exceptions.Value("cannot assign a value of type {} to coin outputs".format(type(value)))

    def coin_input_add(self, parentid, fulfillment, parent_output=None):
        ci = CoinInput(parentid=parentid, fulfillment=fulfillment)
        ci.parent_output = parent_output
        self._coin_inputs.append(ci)

    def refund_coin_output_set(self, value, condition, id=None):
        co = CoinOutput(value=value, condition=condition)
        co.id = id
        self._refund_coin_output = co

    @property
    def addresses(self):
        """
        Network addresses that will be part of the 3Bot Registration.
        """
        return self._addresses

    @addresses.setter
    def addresses(self, value):
        self._addresses = []
        if not value:
            return
        for address in value:
            self.address_add(address)

    def address_add(self, address):
        """
        Add a NetworkAddress that will be added as part of the 3Bot Registration.
        """
        if len(self._addresses) == BotTransactionBaseClass.MAX_ADDRESSES_PER_BOT:
            raise Exception(
                "a 3Bot can have a maximum of {} addresses, there is no more space for {} ({})".format(
                    BotTransactionBaseClass.MAX_ADDRESSES_PER_BOT, address, type(address)
                )
            )
        self._addresses.append(NetworkAddress(address=address))

    @property
    def names(self):
        """
        Bot names that will be part of the 3Bot Registration.
        """
        return self._names

    @names.setter
    def names(self, value):
        self._names = []
        if not value:
            return
        for name in value:
            self.name_add(name)

    def name_add(self, name):
        """
        Add a BotName that will be added as part of the 3Bot Registration.
        """
        if len(self._names) == BotTransactionBaseClass.MAX_NAMES_PER_BOT:
            raise Exception(
                "a 3Bot can have a maximum of {} names, there is no more space for {} ({})".format(
                    BotTransactionBaseClass.MAX_NAMES_PER_BOT, name, type(name)
                )
            )
        self._names.append(BotName(value=name))

    @property
    def transaction_fee(self):
        if self._transaction_fee is None:
            return Currency()
        return self._transaction_fee

    @transaction_fee.setter
    def transaction_fee(self, txfee):
        if txfee is None:
            self._transaction_fee = None
        else:
            self._transaction_fee = Currency(value=txfee)

    @property
    def miner_fees(self):
        if self._transaction_fee is None:
            return []
        return [self._transaction_fee]

    @property
    def number_of_months(self):
        return self._number_of_months

    @number_of_months.setter
    def number_of_months(self, n):
        if n < 1 or n > 24:
            raise j.exceptions.Value(
                "number of months for a 3Bot Registration Transaction has to be in the inclusive range [1,24]"
            )
        self._number_of_months = n

    @property
    def signature(self):
        if self._signature is None:
            return ED25519Signature(as_array=True)
        return self._signature

    @signature.setter
    def signature(self, value):
        if value is None:
            self._signature = None
            return
        self._signature = ED25519Signature(value=value, as_array=True)

    @property
    def public_key(self):
        if self._public_key is None:
            return PublicKey()
        return self._public_key

    @public_key.setter
    def public_key(self, value):
        if value is None:
            self._public_key = None
            return
        if not isinstance(value, PublicKey):
            raise j.exceptions.Value(
                "cannot assign value of type {} as BotRegistration's public key (expected type: PublicKey)".format(
                    type(value)
                )
            )
        self._public_key = PublicKey(specifier=value.specifier, hash=value.hash)

    def signature_add(self, public_key, signature):
        """
        Implements SignatureCallbackBase.
        """
        if self._public_key.unlockhash != public_key.unlockhash:
            raise j.exceptions.Value(
                "given public key ({}) does not equal public key ({})".format(
                    str(self._public_key.unlockhash), str(public_key.unlockhash)
                )
            )
        self.signature = signature

    def _signature_hash_input_get(self, *extra_objects):
        e = j.data.rivine.encoder_rivine_get()

        # encode the transaction version
        e.add_int8(self.version)

        # encode the specifier
        e.add_array(TransactionV144._SPECIFIER)

        # extra objects if any
        if extra_objects:
            e.add_all(*extra_objects)

        # encode addresses, names and number of months
        e.add_all(self.addresses, self.names)
        e.add_int8(self.number_of_months)

        # encode coin inputs
        e.add(len(self.coin_inputs))
        for ci in self.coin_inputs:
            e.add(ci.parentid)

        # encode transaction fee
        e.add_all(self.transaction_fee)

        # encode refund coin output
        if self._refund_coin_output is None:
            e.add_int8(0)
        else:
            e.add_int8(1)
            e.add(self._refund_coin_output)

        # encode public key
        e.add(self.public_key)

        # return data
        return e.data

    def _id_input_compute(self):
        return bytearray(TransactionV144._SPECIFIER) + self._binary_encode_data()

    def _binary_encode_data(self):
        e = j.data.rivine.encoder_rivine_get()

        # get addresses and names
        addresses = self.addresses
        names = self.names
        addresses_length = len(addresses)
        names_length = len(names)

        # encode bot binary encoding prefix (containing length and refund info)
        maf = BotMonthsAndFlagsData(
            number_of_months=self.number_of_months,
            has_addresses=(addresses_length > 0),
            has_names=(names_length > 0),
            has_refund=(self._refund_coin_output is not None),
        )
        e.add(maf)
        # encode the address and name length
        e.add_int8(addresses_length | (names_length << 4))

        # encode all addresses and names
        e.add_array(addresses)
        e.add_array(names)

        # encode transaction fee and coin inputs
        e.add_all(self.transaction_fee, self.coin_inputs)

        # encode refund coin output, if defined
        if maf.has_refund:
            e.add(self._refund_coin_output)

        # encode the identification at the end
        e.add_all(self.public_key, self.signature)

        # return encoded data
        return e.data

    def _from_json_data_object(self, data):
        self._addresses = [NetworkAddress.from_json(address) for address in data.get("addresses", []) or []]
        self._names = [BotName.from_json(name) for name in data.get("names", []) or []]
        self._number_of_months = int(data.get("nrofmonths", 0) or 0)
        if "txfee" in data:
            self._transaction_fee = Currency.from_json(data["txfee"])
        else:
            self._transaction_fee = None
        self._coin_inputs = [CoinInput.from_json(ci) for ci in data.get("coininputs", []) or []]
        if "refundcoinoutput" in data:
            self._refund_coin_output = CoinOutput.from_json(data["refundcoinoutput"])
        else:
            self._refund_coin_output = None
        if "identification" not in data or data["identification"] in (None, {}):
            self._public_key = None
            self._signature = None
        else:
            identification = data["identification"]
            self._public_key = PublicKey.from_json(identification["publickey"])
            self._signature = ED25519Signature.from_json(identification["signature"], as_array=True)

    def _json_data_object(self):
        output = {
            "nrofmonths": self.number_of_months,
            "txfee": self.transaction_fee.json(),
            "coininputs": [ci.json() for ci in self.coin_inputs],
            "identification": {"publickey": self._public_key.json(), "signature": self._signature.json()},
        }
        addresses = self.addresses
        if len(addresses) > 0:
            output["addresses"] = [address.json() for address in addresses]
        names = self.names
        if len(names) > 0:
            output["names"] = [name.json() for name in names]
        if self._refund_coin_output is not None:
            output["refundcoinoutput"] = self._refund_coin_output.json()
        return output

    def _extra_signature_requests_new(self):
        if self._public_key is None:
            # if no parent public key is defined, cannot do anything
            return []
        if self._signature is not None:
            return []  # nothing to do
        # generate the input hash func
        input_hash_func = InputSignatureHashFactory(self, BotTransactionBaseClass.SPECIFIER_SENDER).signature_hash_new
        # define the input_hash_new generator function,
        # used to create the input hash for creating the signature
        unlockhash = self._public_key.unlockhash

        def input_hash_gen(public_key):
            return input_hash_func()

        # create the only signature request
        return [SignatureRequest(unlockhash=unlockhash, input_hash_gen=input_hash_gen, callback=self)]

    def _extra_is_fulfilled(self):
        return self._signature is not None


class TransactionV145(BotTransactionBaseClass):
    _SPECIFIER = b"bot recupdate tx"

    def __init__(self):
        self._botid = None
        self._addresses_to_add = []
        self._addresses_to_remove = []
        self._names_to_add = []
        self._names_to_remove = []
        self._number_of_months = 0
        self._transaction_fee = None
        self._coin_inputs = []
        self._refund_coin_output = None
        self._signature = None
        self._parent_public_key = None

        super().__init__()

    @property
    def version(self):
        return TransactionVersion.THREEBOT_RECORD_UPDATE

    @property
    def required_bot_fees(self):
        """
        The fees required to pay for this 3Bot Record Update Transaction.
        """
        fees = Currency(value=0)
        # all months have to be paid
        if self._number_of_months > 0:
            fees += BotTransactionBaseClass.compute_monthly_bot_fees(self._number_of_months)
        # if addresses have been modified, this has to be paid
        if len(self._addresses_to_add) > 0 or len(self._addresses_to_remove) > 0:
            fees += BotTransactionBaseClass.BOT_FEE_NETWORK_ADDRESS_UPDATE
        # each additional that is added, has to be paid as well
        lnames = len(self._names_to_add)
        if lnames > 0:
            fees += BotTransactionBaseClass.BOT_FEE_ADDITIONAL_NAME * lnames
        # return the total fees
        return fees

    @property
    def botid(self):
        if self._botid is None:
            return 0
        return self._botid

    @botid.setter
    def botid(self, value):
        if value is None:
            self._botid = None
        elif isinstance(value, int):
            if value <= 0:
                raise j.exceptions.Value("a bot identifier has to be at least equal to 1: {} is invalid".format(value))
            self._botid = value
        else:
            raise j.exceptions.Value("a bot identifier has to be an integer, cannot be of type {}".format(type(value)))

    @property
    def coin_inputs(self):
        """
        Coin inputs of this Transaction,
        used as funding for coin outputs, fees and any other kind of coin output.
        """
        return self._coin_inputs

    @coin_inputs.setter
    def coin_inputs(self, value):
        self._coin_inputs = []
        if not value:
            return
        for ci in value:
            self.coin_input_add(ci.parentid, ci.fulfillment, parent_output=ci.parent_output)

    @property
    def refund_coin_output(self):
        if self._refund_coin_output is None:
            return CoinOutput()
        return self._refund_coin_output

    @property
    def coin_outputs(self):
        """
        Empty list, or a singleton with the refund coin output if that one exists.
        """
        if self._refund_coin_output is None:
            return []
        return [self._refund_coin_output]

    @coin_outputs.setter
    def coin_outputs(self, value):
        if isinstance(value, list):
            lvalue = len(value)
            if lvalue == 0:
                value = None
            elif lvalue == 1:
                value = value[0]
            else:
                raise j.exceptions.Value("ThreeBot only can have one coin output, a refund coin output")
        if value is None:
            self._refund_coin_output = None
        elif isinstance(value, CoinOutput):
            self._refund_coin_output = CoinOutput(value=value.value, condition=value.condition)
            self._refund_coin_output.id = value.id
        else:
            raise j.exceptions.Value("cannot assign a value of type {} to coin outputs".format(type(value)))

    def coin_input_add(self, parentid, fulfillment, parent_output=None):
        ci = CoinInput(parentid=parentid, fulfillment=fulfillment)
        ci.parent_output = parent_output
        self._coin_inputs.append(ci)

    def refund_coin_output_set(self, value, condition, id=None):
        co = CoinOutput(value=value, condition=condition)
        co.id = id
        self._refund_coin_output = co

    @property
    def addresses_to_add(self):
        """
        Network addresses that will be added to the 3Bot's record.
        """
        return self._addresses_to_add

    @addresses_to_add.setter
    def addresses_to_add(self, value):
        self._addresses_to_add = []
        if not value:
            return
        for address in value:
            self.address_add(address)

    def address_add(self, address):
        """
        Add a NetworkAddress that will be added to the 3Bot's record.
        """
        if len(self._addresses_to_add) == BotTransactionBaseClass.MAX_ADDRESSES_PER_BOT:
            raise Exception(
                "a 3Bot can have a maximum of {} addresses, there is no more space for {} ({})".format(
                    BotTransactionBaseClass.MAX_ADDRESSES_PER_BOT, address, type(address)
                )
            )
        self._addresses_to_add.append(NetworkAddress(address=address))

    @property
    def addresses_to_remove(self):
        """
        Network addresses that will be removed from the 3Bot's record.
        """
        return self._addresses_to_remove

    @addresses_to_remove.setter
    def addresses_to_remove(self, value):
        self._addresses_to_remove = []
        if not value:
            return
        for address in value:
            self.address_remove(address)

    def address_remove(self, address):
        """
        Add a NetworkAddress that will be removed from the 3Bot's record.
        """
        if len(self._addresses_to_remove) == BotTransactionBaseClass.MAX_ADDRESSES_PER_BOT:
            raise Exception(
                "a 3Bot can have a maximum of {} addresses, there is no more space for {} ({})".format(
                    BotTransactionBaseClass.MAX_ADDRESSES_PER_BOT, address, type(address)
                )
            )
        self._addresses_to_remove.append(NetworkAddress(address=address))

    @property
    def names_to_add(self):
        """
        Bot names that will added to the 3Bot's record.
        """
        return self._names_to_add

    @names_to_add.setter
    def names_to_add(self, value):
        self._names_to_add = []
        if not value:
            return
        for name in value:
            self.name_add(name)

    def name_add(self, name):
        """
        Add a BotName that will be added to the 3Bot's record.
        """
        if len(self._names_to_add) == BotTransactionBaseClass.MAX_NAMES_PER_BOT:
            raise Exception(
                "a 3Bot can have a maximum of {} names, there is no more space for {} ({})".format(
                    BotTransactionBaseClass.MAX_NAMES_PER_BOT, name, type(name)
                )
            )
        self._names_to_add.append(BotName(value=name))

    @property
    def names_to_remove(self):
        """
        Bot names that will be removed from the 3Bot's record
        """
        return self._names_to_remove

    @names_to_remove.setter
    def names_to_remove(self, value):
        self._names_to_remove = []
        if not value:
            return
        for name in value:
            self.name_remove(name)

    def name_remove(self, name):
        """
        Add a BotName that will be removed from the 3Bot's record.
        """
        if len(self._names_to_remove) == BotTransactionBaseClass.MAX_NAMES_PER_BOT:
            raise Exception(
                "a 3Bot can have a maximum of {} names, there is no more space for {} ({})".format(
                    BotTransactionBaseClass.MAX_NAMES_PER_BOT, name, type(name)
                )
            )
        self._names_to_remove.append(BotName(value=name))

    @property
    def transaction_fee(self):
        if self._transaction_fee is None:
            return Currency()
        return self._transaction_fee

    @transaction_fee.setter
    def transaction_fee(self, txfee):
        if txfee is None:
            self._transaction_fee = None
        else:
            self._transaction_fee = Currency(value=txfee)

    @property
    def miner_fees(self):
        if self._transaction_fee is None:
            return []
        return [self._transaction_fee]

    @property
    def number_of_months(self):
        return self._number_of_months

    @number_of_months.setter
    def number_of_months(self, n):
        if n < 0 or n > 24:
            raise j.exceptions.Value(
                "number of months for a 3Bot Record Update has to be in the inclusive range [0,24]"
            )
        self._number_of_months = n

    @property
    def signature(self):
        if self._signature is None:
            return ED25519Signature(as_array=True)
        return self._signature

    @signature.setter
    def signature(self, value):
        if value is None:
            self._signature = None
            return
        self._signature = ED25519Signature(value=value, as_array=True)

    @property
    def parent_public_key(self):
        if self._parent_public_key is None:
            return PublicKey()
        return self._parent_public_key

    @parent_public_key.setter
    def parent_public_key(self, value):
        if value is None:
            self._parent_public_key = None
            return
        if not isinstance(value, PublicKey):
            raise j.exceptions.Value(
                "cannot assign value of type {} as BotRecordUpdateTransactions's parent public key (expected type: PublicKey)".format(
                    type(value)
                )
            )
        self._parent_public_key = PublicKey(specifier=value.specifier, hash=value.hash)

    def signature_add(self, public_key, signature):
        """
        Implements SignatureCallbackBase.
        """
        if self._parent_public_key.unlockhash != public_key.unlockhash:
            raise j.exceptions.Value(
                "given public key ({}) does not equal parent public key ({})".format(
                    str(self._parent_public_key.unlockhash), str(public_key.unlockhash)
                )
            )
        self.signature = signature

    def _signature_hash_input_get(self, *extra_objects):
        e = j.data.rivine.encoder_rivine_get()

        # encode the transaction version
        e.add_int8(self.version)

        # encode the specifier
        e.add_array(TransactionV145._SPECIFIER)

        # encode the botID
        e.add_int32(self.botid)

        # extra objects if any
        if extra_objects:
            e.add_all(*extra_objects)

        # encode addresses, names and number of months
        e.add_all(self.addresses_to_add, self.addresses_to_remove)
        e.add_all(self.names_to_add, self.names_to_remove)
        e.add_int8(self.number_of_months)

        # encode coin inputs
        e.add(len(self.coin_inputs))
        for ci in self.coin_inputs:
            e.add(ci.parentid)

        # encode transaction fee
        e.add_all(self.transaction_fee)

        # encode refund coin output
        if self._refund_coin_output is None:
            e.add_int8(0)
        else:
            e.add_int8(1)
            e.add(self._refund_coin_output)

        # return data
        return e.data

    def _id_input_compute(self):
        return bytearray(TransactionV145._SPECIFIER) + self._binary_encode_data()

    def _binary_encode_data(self):
        e = j.data.rivine.encoder_rivine_get()

        # get addresses and names
        addresses_to_add = self.addresses_to_add
        addresses_to_remove = self.addresses_to_remove
        names_to_add = self.names_to_add
        names_to_remove = self.names_to_remove
        addresses_to_add_length = len(addresses_to_add)
        addresses_to_remove_length = len(addresses_to_remove)
        names_to_add_length = len(names_to_add)
        names_to_remove_length = len(names_to_remove)

        # encode the identifier
        e.add_int32(self.botid)

        # encode bot binary encoding prefix (containing length and refund info)
        maf = BotMonthsAndFlagsData(
            number_of_months=self.number_of_months,
            has_addresses=(addresses_to_add_length > 0 or addresses_to_remove_length > 0),
            has_names=(names_to_add_length > 0 or names_to_remove_length > 0),
            has_refund=(self._refund_coin_output is not None),
        )
        e.add(maf)

        # if we have addresses, encode it
        if maf.has_addresses:
            e.add_int8(addresses_to_add_length | (addresses_to_remove_length << 4))
            e.add_array(addresses_to_add)
            e.add_array(addresses_to_remove)

        # if we have names, encode it
        if maf.has_names:
            e.add_int8(names_to_add_length | (names_to_remove_length << 4))
            e.add_array(names_to_add)
            e.add_array(names_to_remove)

        # encode transaction fee and coin inputs
        e.add_all(self.transaction_fee, self.coin_inputs)

        # encode refund coin output, if defined
        if maf.has_refund:
            e.add(self._refund_coin_output)

        # encode the signature at the end
        e.add(self.signature)

        # return encoded data
        return e.data

    def _from_json_data_object(self, data):
        self._botid = int(data.get("id", 0) or 0)
        addresses = data.get("addresses", {}) or {}
        self._addresses_to_add = [NetworkAddress.from_json(address) for address in addresses.get("add", []) or []]
        self._addresses_to_remove = [NetworkAddress.from_json(address) for address in addresses.get("remove", []) or []]
        names = data.get("names", {}) or {}
        self._names_to_add = [BotName.from_json(name) for name in names.get("add", []) or []]
        self._names_to_remove = [BotName.from_json(name) for name in names.get("remove", []) or []]
        self._number_of_months = int(data.get("nrofmonths", 0) or 0)
        if "txfee" in data:
            self._transaction_fee = Currency.from_json(data["txfee"])
        else:
            self._transaction_fee = None
        self._coin_inputs = [CoinInput.from_json(ci) for ci in data.get("coininputs", []) or []]
        if "refundcoinoutput" in data:
            self._refund_coin_output = CoinOutput.from_json(data["refundcoinoutput"])
        else:
            self._refund_coin_output = None
        self._signature = ED25519Signature.from_json(data.get("signature", None) or None)

    def _json_data_object(self):
        output = {
            "id": self.botid,
            "nrofmonths": self.number_of_months,
            "txfee": self.transaction_fee.json(),
            "coininputs": [ci.json() for ci in self.coin_inputs],
            "signature": self.signature.json(),
        }
        # encode addresses
        addresses_to_add = self.addresses_to_add
        addresses_to_remove = self.addresses_to_remove
        addresses_to_add_length = len(addresses_to_add)
        addresses_to_remove_length = len(addresses_to_remove)
        if addresses_to_add_length > 0:
            output["addresses"] = {"add": [address.json() for address in addresses_to_add]}
        if addresses_to_remove_length > 0:
            d = output.get("addresses", {})
            d["remove"] = [address.json() for address in addresses_to_remove]
            output["addresses"] = d

        # encode names
        names_to_add = self.names_to_add
        names_to_remove = self.names_to_remove
        names_to_add_length = len(names_to_add)
        names_to_remove_length = len(names_to_remove)
        if names_to_add_length > 0:
            output["names"] = {"add": [name.json() for name in names_to_add]}
        if names_to_remove_length > 0:
            d = output.get("names", {})
            d["remove"] = [name.json() for name in names_to_remove]
            output["names"] = d

        # encode refund coin output
        if self._refund_coin_output is not None:
            output["refundcoinoutput"] = self._refund_coin_output.json()
        return output

    def _extra_signature_requests_new(self):
        if self._parent_public_key is None:
            # if no parent public key is defined, cannot do anything
            return []
        if self._signature is not None:
            return []  # nothing to do
        # generate the input hash func
        input_hash_func = InputSignatureHashFactory(self, BotTransactionBaseClass.SPECIFIER_SENDER).signature_hash_new
        # define the input_hash_new generator function,
        # used to create the input hash for creating the signature
        unlockhash = self._parent_public_key.unlockhash

        def input_hash_gen(public_key):
            return input_hash_func()

        # create the only signature request
        return [SignatureRequest(unlockhash=unlockhash, input_hash_gen=input_hash_gen, callback=self)]

    def _extra_is_fulfilled(self):
        return self._signature is not None


class TransactionV146(BotTransactionBaseClass):
    _SPECIFIER = b"bot nametrans tx"

    def __init__(self):
        self._sender_botid = None
        self._receiver_botid = None
        self._names = []
        self._transaction_fee = None
        self._coin_inputs = None
        self._refund_coin_output = None
        self._sender_signature = None
        self._receiver_signature = None
        self._sender_parent_public_key = None
        self._receiver_parent_public_key = None

        super().__init__()

    @property
    def version(self):
        return TransactionVersion.THREEBOT_NAME_TRANSFER

    @property
    def required_bot_fees(self):
        """
        The fees required to pay for this 3Bot Name Transfer Transaction.
        """
        return BotTransactionBaseClass.BOT_FEE_ADDITIONAL_NAME * len(self.names)

    @property
    def sender_botid(self):
        if self._sender_botid is None:
            return 0
        return self._sender_botid

    @sender_botid.setter
    def sender_botid(self, value):
        if value is None:
            self._sender_botid = None
        elif isinstance(value, int):
            if value <= 0:
                raise j.exceptions.Value(
                    "a (sender) bot identifier has to be at least equal to 1: {} is invalid".format(value)
                )
            self._sender_botid = value
        else:
            raise j.exceptions.Value(
                "a (sender) bot identifier has to be an integer, cannot be of type {}".format(type(value))
            )

    @property
    def receiver_botid(self):
        if self._receiver_botid is None:
            return 0
        return self._receiver_botid

    @receiver_botid.setter
    def receiver_botid(self, value):
        if value is None:
            self._receiver_botid = None
        elif isinstance(value, int):
            if value <= 0:
                raise j.exceptions.Value(
                    "a (receiver) bot identifier has to be at least equal to 1: {} is invalid".format(value)
                )
            self._receiver_botid = value
        else:
            raise j.exceptions.Value(
                "a (receiver) bot identifier has to be an integer, cannot be of type {}".format(type(value))
            )

    @property
    def coin_inputs(self):
        """
        Coin inputs of this Transaction,
        used as funding for coin outputs, fees and any other kind of coin output.
        """
        return self._coin_inputs

    @coin_inputs.setter
    def coin_inputs(self, value):
        self._coin_inputs = []
        if not value:
            return
        for ci in value:
            self.coin_input_add(ci.parentid, ci.fulfillment, parent_output=ci.parent_output)

    @property
    def refund_coin_output(self):
        if self._refund_coin_output is None:
            return CoinOutput()
        return self._refund_coin_output

    @property
    def coin_outputs(self):
        """
        Empty list, or a singleton with the refund coin output if that one exists.
        """
        if self._refund_coin_output is None:
            return []
        return [self._refund_coin_output]

    @coin_outputs.setter
    def coin_outputs(self, value):
        if isinstance(value, list):
            lvalue = len(value)
            if lvalue == 0:
                value = None
            elif lvalue == 1:
                value = value[0]
            else:
                raise j.exceptions.Value("ThreeBot only can have one coin output, a refund coin output")
        if value is None:
            self._refund_coin_output = None
        elif isinstance(value, CoinOutput):
            self._refund_coin_output = CoinOutput(value=value.value, condition=value.condition)
            self._refund_coin_output.id = value.id
        else:
            raise j.exceptions.Value("cannot assign a value of type {} to coin outputs".format(type(value)))

    def coin_input_add(self, parentid, fulfillment, parent_output=None):
        ci = CoinInput(parentid=parentid, fulfillment=fulfillment)
        ci.parent_output = parent_output
        self._coin_inputs.append(ci)

    def refund_coin_output_set(self, value, condition, id=None):
        co = CoinOutput(value=value, condition=condition)
        co.id = id
        self._refund_coin_output = co

    @property
    def names(self):
        """
        Bot names that will be transfered from the sender- to the receiver 3Bot.
        """
        return self._names

    @names.setter
    def names(self, value):
        self._names_to_add = []
        if not value:
            return
        for name in value:
            self.name_add(name)

    def name_add(self, name):
        """
        Add a BotName that will be tranfered from the sender- to the receiver 3Bot.
        """
        if len(self._names) == BotTransactionBaseClass.MAX_NAMES_PER_BOT:
            raise Exception(
                "a 3Bot can have a maximum of {} names, there is no more space for {} ({})".format(
                    BotTransactionBaseClass.MAX_NAMES_PER_BOT, name, type(name)
                )
            )
        self._names.append(BotName(value=name))

    @property
    def transaction_fee(self):
        if self._transaction_fee is None:
            return Currency()
        return self._transaction_fee

    @transaction_fee.setter
    def transaction_fee(self, txfee):
        if txfee is None:
            self._transaction_fee = None
        else:
            self._transaction_fee = Currency(value=txfee)

    @property
    def miner_fees(self):
        if self._transaction_fee is None:
            return []
        return [self._transaction_fee]

    @property
    def sender_signature(self):
        if self._sender_signature is None:
            return ED25519Signature(as_array=True)
        return self._sender_signature

    @sender_signature.setter
    def sender_signature(self, value):
        if value is None:
            self._sender_signature = None
            return
        self._sender_signature = ED25519Signature(value=value, as_array=True)

    @property
    def receiver_signature(self):
        if self._receiver_signature is None:
            return ED25519Signature(as_array=True)
        return self._receiver_signature

    @receiver_signature.setter
    def receiver_signature(self, value):
        if value is None:
            self._receiver_signature = None
            return
        self._receiver_signature = ED25519Signature(value=value, as_array=True)

    @property
    def sender_parent_public_key(self):
        if self._sender_parent_public_key is None:
            return PublicKey()
        return self._sender_parent_public_key

    @sender_parent_public_key.setter
    def sender_parent_public_key(self, value):
        if value is None:
            self._sender_parent_public_key = None
            return
        if not isinstance(value, PublicKey):
            raise j.exceptions.Value(
                "cannot assign value of type {} as BotNameTransferTransaction's sender parent public key (expected type: PublicKey)".format(
                    type(value)
                )
            )
        self._sender_parent_public_key = PublicKey(specifier=value.specifier, hash=value.hash)

    @property
    def receiver_parent_public_key(self):
        if self._receiver_parent_public_key is None:
            return PublicKey()
        return self._receiver_parent_public_key

    @receiver_parent_public_key.setter
    def receiver_parent_public_key(self, value):
        if value is None:
            self._receiver_parent_public_key = None
            return
        if not isinstance(value, PublicKey):
            raise j.exceptions.Value(
                "cannot assign value of type {} as BotNameTransferTransaction's receiver parent public key (expected type: PublicKey)".format(
                    type(value)
                )
            )
        self._receiver_parent_public_key = PublicKey(specifier=value.specifier, hash=value.hash)

    def signature_add(self, public_key, signature):
        """
        Implements SignatureCallbackBase.
        """
        unlockhash = public_key.unlockhash
        if unlockhash == self.sender_parent_public_key.unlockhash:
            self.sender_signature = signature
        elif unlockhash == self.receiver_parent_public_key.unlockhash:
            self.receiver_signature = signature
        else:
            raise j.exceptions.Value(
                "given public key (unlockhash: {}) is not linked to this BotNameTransfer Transaction".format(
                    str(unlockhash)
                )
            )

    def _signature_hash_input_get(self, *extra_objects):
        e = j.data.rivine.encoder_rivine_get()

        # encode the transaction version
        e.add_int8(self.version)

        # encode the specifier
        e.add_array(TransactionV146._SPECIFIER)

        # encode the bot identifiers
        e.add_int32(self.sender_botid)
        e.add_int32(self.receiver_botid)

        # extra objects if any
        if extra_objects:
            e.add_all(*extra_objects)

        # encode names
        e.add(self.names)

        # encode coin inputs
        e.add(len(self.coin_inputs))
        for ci in self.coin_inputs:
            e.add(ci.parentid)

        # encode transaction fee
        e.add(self.transaction_fee)

        # encode refund coin output
        if self._refund_coin_output is None:
            e.add_int8(0)
        else:
            e.add_int8(1)
            e.add(self._refund_coin_output)

        # return data
        return e.data

    def _id_input_compute(self):
        return bytearray(TransactionV146._SPECIFIER) + self._binary_encode_data()

    def _binary_encode_data(self):
        e = j.data.rivine.encoder_rivine_get()

        # get names
        names = self.names
        names_length = len(names)
        info_value = names_length

        # get has refund status
        has_refund = False
        if self._refund_coin_output is not None:
            has_refund = True
            info_value |= 16

        # encode sender bot info
        e.add_int32(self.sender_botid)
        e.add(self.sender_signature)

        # encode receiver bot info
        e.add_int32(self.receiver_botid)
        e.add(self.receiver_signature)

        # encode info value
        e.add_int8(info_value)

        # encode the names
        e.add_array(names)

        # encode transaction fee and coin inputs
        e.add_all(self.transaction_fee, self.coin_inputs)

        # encode refund coin output, if defined
        if has_refund:
            e.add(self._refund_coin_output)

        # return encoded data
        return e.data

    def _from_json_data_object(self, data):
        # decode sender info
        if "sender" in data:
            bot_data = data["sender"]
            self._sender_botid = int(bot_data.get("id", 0) or 0)
            self._sender_signature = ED25519Signature.from_json(bot_data.get("signature", None) or None)
        else:
            self._sender_botid = None
            self._sender_signature = None
        # decode receiver info
        if "receiver" in data:
            bot_data = data["receiver"]
            self._receiver_botid = int(bot_data.get("id", 0) or 0)
            self._receiver_signature = ED25519Signature.from_json(bot_data.get("signature", None) or None)
        else:
            self._receiver_botid = None
            self._receiver_signature = None
        # decode names
        self._names = [BotName.from_json(name) for name in data.get("names", []) or []]
        # decode transaction fee
        if "txfee" in data:
            self._transaction_fee = Currency.from_json(data["txfee"])
        else:
            self._transaction_fee = None
        # decode coin inputs
        self._coin_inputs = [CoinInput.from_json(ci) for ci in data.get("coininputs", []) or []]
        # decode refund coin output
        if "refundcoinoutput" in data:
            self._refund_coin_output = CoinOutput.from_json(data["refundcoinoutput"])
        else:
            self._refund_coin_output = None

    def _json_data_object(self):
        output = {
            "sender": {"id": self.sender_botid, "signature": self.sender_signature.json()},
            "receiver": {"id": self.receiver_botid, "signature": self.receiver_signature.json()},
            "names": [name.json() for name in self.names],
            "txfee": self.transaction_fee.json(),
            "coininputs": [ci.json() for ci in self.coin_inputs],
        }
        if self._refund_coin_output is not None:
            output["refundcoinoutput"] = self._refund_coin_output.json()
        return output

    def _extra_signature_requests_new(self):
        requests = []
        # collect, if possible, the sender request
        request = self._extra_signature_requests_for(
            self._sender_parent_public_key, self._sender_signature, BotTransactionBaseClass.SPECIFIER_SENDER
        )
        if request is not None:
            requests.append(request)
        # collect, if possible, the receiver request
        request = self._extra_signature_requests_for(
            self._receiver_parent_public_key, self._receiver_signature, BotTransactionBaseClass.SPECIFIER_RECEIVER
        )
        if request is not None:
            requests.append(request)
        # return all requests, if any
        return requests

    def _extra_signature_requests_for(self, public_key, signature, specifier):
        if public_key is None:
            # if no parent public key is defined, cannot do anything
            return None
        if signature is not None:
            return None
        # generate the input hash func
        factory = InputSignatureHashFactory(self, specifier)
        # define the input_hash_new generator function,
        # used to create the input hash for creating the signature
        unlockhash = public_key.unlockhash
        # create the only signature request
        return SignatureRequest(
            unlockhash=unlockhash, input_hash_gen=(lambda public_key: factory.signature_hash_new()), callback=self
        )

    def _extra_is_fulfilled(self):
        return self._sender_signature is not None and self._receiver_signature is not None
