from Jumpscale import j

from .Base import TransactionBaseClass, TransactionVersion, InputSignatureHashFactory

from ..FulfillmentTypes import ED25519Signature, SignatureCallbackBase, SignatureRequest
from ..ConditionTypes import UnlockHash, ConditionUnlockHash
from ..PrimitiveTypes import BinaryData, Currency
from ..ERC20 import ERC20Address, ERC20Hash
from ..IO import CoinInput, CoinOutput
from ..CryptoTypes import PublicKey


class TransactionV208(TransactionBaseClass):
    _SPECIFIER = b"erc20 convert tx"

    def __init__(self):
        self._address = None
        self._value = None
        self._transaction_fee = None
        self._coin_inputs = []
        self._refund_coin_output = None

        super().__init__()

    @property
    def version(self):
        return TransactionVersion.ERC20_CONVERT

    @property
    def address(self):
        if self._address is None:
            return ERC20Address()
        return self._address

    @address.setter
    def address(self, value):
        if value is None:
            self._address = None
        else:
            self._address = ERC20Address(value=value)

    @property
    def value(self):
        if self._value is None:
            return Currency()
        return self._value

    @value.setter
    def value(self, value):
        if value is None:
            self._value = None
        else:
            self._value = Currency(value=value)

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

    def _signature_hash_input_get(self, *extra_objects):
        e = j.data.rivine.encoder_rivine_get()

        # encode the transaction version
        e.add_int8(self.version)

        # encode the specifier
        e.add_array(TransactionV208._SPECIFIER)

        # encode the address and value
        e.add_all(self.address, self.value)

        # extra objects if any
        if extra_objects:
            e.add_all(*extra_objects)

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
        return bytearray(TransactionV208._SPECIFIER) + self._binary_encode_data()

    def _binary_encode_data(self):
        e = j.data.rivine.encoder_rivine_get()
        # encode all easy properties
        e.add_all(self.address, self.value, self.transaction_fee, self.coin_inputs)
        # encode the only "pointer" property
        if self._refund_coin_output is None:
            e.add_int8(0)
        else:
            e.add_int8(1)
            e.add(self._refund_coin_output)

        # return encoded data
        return e.data

    def _from_json_data_object(self, data):
        # decode address
        if "address" in data:
            self._address = ERC20Address.from_json(data["address"])
        else:
            self._address = None
        # decode value
        if "value" in data:
            self._value = Currency.from_json(data["value"])
        else:
            self._value = None
        # decode transaction fee
        if "txfee" in data:
            self._transaction_fee = Currency.from_json(data["txfee"])
        else:
            self._transaction_fee = None
        # decode coin inputs
        self._coin_inputs = [CoinInput.from_json(ci) for ci in data.get("coininputs", []) or []]
        # decode refund coin output (if it exists)
        if "refundcoinoutput" in data:
            self._refund_coin_output = CoinOutput.from_json(data["refundcoinoutput"])
        else:
            self._refund_coin_output = None

    def _json_data_object(self):
        output = {
            "address": self.address.json(),
            "value": self.value.json(),
            "coininputs": [ci.json() for ci in self.coin_inputs],
            "txfee": self.transaction_fee.json(),
        }
        if self._refund_coin_output is not None:
            output["refundcoinoutput"] = self._refund_coin_output.json()
        return output


class TransactionV209(TransactionBaseClass):
    _SPECIFIER = b"erc20 coingen tx"

    def __init__(self):
        self._address = None
        self._value = None
        self._transaction_fee = None
        self._blockid = None
        self._transactionid = None

        super().__init__()

    @property
    def version(self):
        return TransactionVersion.ERC20_COIN_CREATION

    @property
    def address(self):
        if self._address is None:
            return UnlockHash()
        return self._address

    @address.setter
    def address(self, value):
        if value is None:
            self._address = None
            return
        if isinstance(value, UnlockHash):
            self._address = value
            return
        self._address = UnlockHash.from_json(value)

    @property
    def value(self):
        if self._value is None:
            return Currency()
        return self._value

    @value.setter
    def value(self, value):
        if value is None:
            self._value = None
        else:
            self._value = Currency(value=value)

    @property
    def blockid(self):
        if self._blockid is None:
            return ERC20Hash()
        return self._blockid

    @blockid.setter
    def blockid(self, value):
        if value is None:
            self._blockid = None
        else:
            self._blockid = ERC20Hash(value=value)

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
    def transactionid(self):
        if self._transactionid is None:
            return ERC20Hash()
        return self._transactionid

    @transactionid.setter
    def transactionid(self, value):
        if value is None:
            self._transactionid = None
        else:
            self._transactionid = ERC20Hash(value=value)

    @property
    def coin_outputs(self):
        """
        A singleton, containing the ERC20-converted TFT coins.
        """
        condition = ConditionUnlockHash(unlockhash=self.address)
        return [CoinOutput(value=self.value, condition=condition, id=None)]

    def _signature_hash_input_get(self, *extra_objects):
        e = j.data.rivine.encoder_sia_get()

        # encode the transaction version
        e.add_array(bytearray([self.version]))

        # encode the specifier
        e.add_array(TransactionV209._SPECIFIER)

        # extra objects if any
        if extra_objects:
            e.add_all(*extra_objects)

        # encode the address and value
        e.add_all(self.address, self.value)

        # encode transaction fee
        e.add_all(self.transaction_fee)

        # encode the block- and transaction identifier
        e.add_all(self.blockid, self.transactionid)

        # return data
        return e.data

    def _id_input_compute(self):
        return bytearray(TransactionV209._SPECIFIER) + self._binary_encode_data()

    def _binary_encode_data(self):
        e = j.data.rivine.encoder_rivine_get()
        # encode all properties
        e.add_all(self.address, self.value, self.transaction_fee, self.blockid, self.transactionid)

        # return encoded data
        return e.data

    def _from_json_data_object(self, data):
        # decode address
        if "address" in data:
            self._address = UnlockHash.from_json(data["address"])
        else:
            self._address = None
        # decode value
        if "value" in data:
            self._value = Currency.from_json(data["value"])
        else:
            self._value = None
        # decode transaction fee
        if "txfee" in data:
            self._transaction_fee = Currency.from_json(data["txfee"])
        else:
            self._transaction_fee = None
        # decode blockid
        if "blockid" in data:
            self._blockid = ERC20Hash.from_json(data["blockid"])
        else:
            self._blockid = None
        # decode transactionid
        if "txid" in data:
            self._transactionid = ERC20Hash.from_json(data["txid"])
        else:
            self._transactionid = None

    def _json_data_object(self):
        return {
            "address": self.address.json(),
            "value": self.value.json(),
            "txfee": self.transaction_fee.json(),
            "blockid": self.blockid.json(),
            "txid": self.transactionid.json(),
        }


class TransactionV210(TransactionBaseClass, SignatureCallbackBase):
    _SPECIFIER = b"erc20 addrreg tx"

    HARDCODED_REGISTRATION_FEE = "10 TFT"
    SPECIFIER_REGISTRATION_SIGNATURE = BinaryData(value=b"registration", fixed_size=0)

    def __init__(self):
        self._public_key = None
        self._signature = None
        self._registration_fee = Currency(value=TransactionV210.HARDCODED_REGISTRATION_FEE)
        self._transaction_fee = None
        self._coin_inputs = None
        self._refund_coin_output = None

        super().__init__()

    @property
    def version(self):
        return TransactionVersion.ERC20_ADDRESS_REGISTRATION

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
    def registration_fee(self):
        return self._registration_fee

    @registration_fee.setter
    def registration_fee(self, txfee):
        if txfee is not None:
            fee = Currency(value=txfee)
            if fee != self._registration_fee:
                raise j.exceptions.Value(
                    "registration fee is hardcoded at {}, cannot be set to {}".format(
                        fee.str(with_unit=True), self._registration_fee.str(with_unit=True)
                    )
                )

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
        e.add_array(TransactionV210._SPECIFIER)

        # encode the public key
        e.add_all(self.public_key)

        # extra objects if any
        if extra_objects:
            e.add_all(*extra_objects)

        # encode coin inputs
        e.add(len(self.coin_inputs))
        for ci in self.coin_inputs:
            e.add(ci.parentid)

        # encode registration and transaction fee
        e.add_all(self.registration_fee, self.transaction_fee)

        # encode refund coin output
        if self._refund_coin_output is None:
            e.add_int8(0)
        else:
            e.add_int8(1)
            e.add(self._refund_coin_output)

        # return data
        return e.data

    def _id_input_compute(self):
        return bytearray(TransactionV210._SPECIFIER) + self._binary_encode_data()

    def _binary_encode_data(self):
        e = j.data.rivine.encoder_rivine_get()
        # encode all easy properties
        e.add_all(self.public_key, self.signature, self.registration_fee, self.transaction_fee, self.coin_inputs)
        # encode the only "pointer" property
        if self._refund_coin_output is None:
            e.add_int8(0)
        else:
            e.add_int8(1)
            e.add(self._refund_coin_output)

        # return encoded data
        return e.data

    def _from_json_data_object(self, data):
        # decode public key
        if "pubkey" in data:
            self._public_key = PublicKey.from_json(data["pubkey"])
        else:
            self._public_key = None
        # decode signature
        if "signature" in data:
            self._signature = ED25519Signature.from_json(data["signature"])
        else:
            self._signature = None
        # decode registration fee
        if "regfee" in data:
            self.registration_fee = Currency.from_json(data["regfee"])
        else:
            self.registration_fee = None
        # decode transaction fee
        if "txfee" in data:
            self._transaction_fee = Currency.from_json(data["txfee"])
        else:
            self._transaction_fee = None
        # decode coin inputs
        self._coin_inputs = [CoinInput.from_json(ci) for ci in data.get("coininputs", []) or []]
        # decode refund coin output (if it exists)
        if "refundcoinoutput" in data:
            self._refund_coin_output = CoinOutput.from_json(data["refundcoinoutput"])
        else:
            self._refund_coin_output = None

    def _json_data_object(self):
        tftaddress = self.public_key.unlockhash
        erc20address = ERC20Address.from_unlockhash(tftaddress)
        output = {
            "pubkey": self.public_key.json(),
            "tftaddress": tftaddress.json(),
            "erc20address": erc20address.json(),
            "signature": self.signature.json(),
            "regfee": self.registration_fee.json(),
            "txfee": self.transaction_fee.json(),
            "coininputs": [ci.json() for ci in self.coin_inputs],
        }
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
        input_hash_func = InputSignatureHashFactory(
            self, TransactionV210.SPECIFIER_REGISTRATION_SIGNATURE
        ).signature_hash_new
        # define the input_hash_new generator function,
        # used to create the input hash for creating the signature
        unlockhash = self._public_key.unlockhash

        def input_hash_gen(public_key):
            return input_hash_func()

        # create the only signature request
        return [SignatureRequest(unlockhash=unlockhash, input_hash_gen=input_hash_gen, callback=self)]

    def _extra_is_fulfilled(self):
        return self._signature is not None
