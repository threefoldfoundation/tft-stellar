from .Base import TransactionBaseClass, TransactionVersion

from ..IO import CoinInput, CoinOutput, BlockstakeInput, BlockstakeOutput
from ..PrimitiveTypes import Currency, BinaryData


class TransactionV1(TransactionBaseClass):
    def __init__(self):
        self._coin_inputs = []
        self._coin_outputs = []
        self._blockstake_inputs = []
        self._blockstake_outputs = []
        self._miner_fees = []
        self._data = BinaryData(strencoding="base64")

        # hidden flag, that indicates if this Txn was a Legacy v0 Txn or not,
        # False by default as we do not wish to produce new legacy Txns, only decode existing ones
        self._legacy = False

        super().__init__()

    @classmethod
    def legacy_from_json(cls, obj):
        """
        Class method to decode v1 Tx from a legacy v0 Tx.
        """

        tv = obj.get("version", -1)
        if TransactionVersion.LEGACY != tv:
            raise Exception(
                "legacy v0 transaction is expected to be of version {}, not version {}".format(
                    TransactionVersion.LEGACY, tv
                )
            )
        txn = cls()

        if "data" not in obj:
            raise Exception(
                "no data object found in Legacy Transaction (v{})".format(TransactionVersion.LEGACY)
            )
        txn_data = obj["data"]
        if "coininputs" in txn_data:
            for legacy_ci_info in txn_data["coininputs"] or []:
                unlocker = legacy_ci_info.get("unlocker", {})
                ci_info = {
                    "parentid": legacy_ci_info.get("parentid", ""),
                    "fulfillment": {
                        "type": 1,
                        "data": {
                            "publickey": unlocker.get("condition", {}).get("publickey"),
                            "signature": unlocker.get("fulfillment", {}).get("signature"),
                        },
                    },
                }
                ci = CoinInput.from_json(ci_info)
                txn._coin_inputs.append(ci)
        if "coinoutputs" in txn_data:
            for legacy_co_info in txn_data["coinoutputs"] or []:
                co_info = {
                    "value": legacy_co_info.get("value", "0"),
                    "condition": {"type": 1, "data": {"unlockhash": legacy_co_info.get("unlockhash", "")}},
                }
                co = CoinOutput.from_json(co_info)
                txn._coin_outputs.append(co)
        if "blockstakeinputs" in txn_data:
            for legacy_bsi_info in txn_data["blockstakeinputs"] or []:
                unlocker = legacy_bsi_info.get("unlocker", {})
                bsi_info = {
                    "parentid": legacy_bsi_info.get("parentid", ""),
                    "fulfillment": {
                        "type": 1,
                        "data": {
                            "publickey": unlocker.get("condition", {}).get("publickey"),
                            "signature": unlocker.get("fulfillment", {}).get("signature"),
                        },
                    },
                }
                bsi = BlockstakeInput.from_json(bsi_info)
                txn._blockstake_inputs.append(bsi)
        if "blockstakeoutputs" in txn_data:
            for legacy_bso_info in txn_data["blockstakeoutputs"] or []:
                bso_info = {
                    "value": legacy_bso_info.get("value", "0"),
                    "condition": {"type": 1, "data": {"unlockhash": legacy_bso_info.get("unlockhash", "")}},
                }
                bso = BlockstakeOutput.from_json(bso_info)
                txn._blockstake_outputs.append(bso)

        if "minerfees" in txn_data:
            for miner_fee in txn_data["minerfees"] or []:
                txn._miner_fees.append(Currency.from_json(miner_fee))
        if "arbitrarydata" in txn_data:
            txn._data = BinaryData.from_json(txn_data.get("arbitrarydata", None) or "", strencoding="base64")

        txn._legacy = True
        return txn

    @property
    def version(self):
        return TransactionVersion.STANDARD

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
    def coin_outputs(self):
        """
        Coin outputs of this Transaction,
        funded by the Transaction's coin inputs.
        """
        return self._coin_outputs

    @coin_outputs.setter
    def coin_outputs(self, value):
        self._coin_outputs = []
        if not value:
            return
        for co in value:
            self.coin_output_add(co.value, co.condition, id=co.id)

    def coin_input_add(self, parentid, fulfillment, parent_output=None):
        ci = CoinInput(parentid=parentid, fulfillment=fulfillment)
        ci.parent_output = parent_output
        self._coin_inputs.append(ci)

    def coin_output_add(self, value, condition, id=None):
        co = CoinOutput(value=value, condition=condition)
        co.id = id
        self._coin_outputs.append(co)

    @property
    def blockstake_inputs(self):
        """
        Blockstake inputs of this Transaction.
        """
        return self._blockstake_inputs

    @blockstake_inputs.setter
    def blockstake_inputs(self, value):
        self._blockstake_inputs = []
        if not value:
            return
        for bsi in value:
            self.blockstake_input_add(bsi.parentid, bsi.fulfillment, parent_output=bsi.parent_output)

    @property
    def blockstake_outputs(self):
        """
        Blockstake outputs of this Transaction.
        """
        return self._blockstake_outputs

    @blockstake_outputs.setter
    def blockstake_outputs(self, value):
        self._blockstake_outputs = []
        if not value:
            return
        for bso in value:
            self.blockstake_output_add(bso.value, bso.condition, id=bso.id)

    def blockstake_input_add(self, parentid, fulfillment, parent_output=None):
        bsi = BlockstakeInput(parentid=parentid, fulfillment=fulfillment)
        bsi.parent_output = parent_output
        self._blockstake_inputs.append(bsi)

    def blockstake_output_add(self, value, condition, id=None):
        bso = BlockstakeOutput(value=value, condition=condition)
        bso.id = id
        self._blockstake_outputs.append(bso)

    def miner_fee_add(self, value):
        self._miner_fees.append(Currency(value=value))

    @property
    def miner_fees(self):
        """
        Miner fees, paid to the block creator of this Transaction,
        funded by this Transaction's coin inputs.
        """
        return self._miner_fees

    @property
    def data(self):
        """
        Optional binary data attached to this Transaction,
        with a max length of 83 bytes.
        """
        if self._data is None:
            return BinaryData(strencoding="base64")
        return self._data

    @data.setter
    def data(self, value):
        if value is None:
            self._data = None
            return
        if isinstance(value, BinaryData):
            value = value.value
        elif isinstance(value, str):
            value = value.encode("utf-8")
        if len(value) > 83:
            raise j.exceptions.Value(
                "arbitrary data can have a maximum bytes length of 83, {} exceeds this limit".format(len(value))
            )
        self._data = BinaryData(value=value, strencoding="base64")

    def _signature_hash_input_get(self, *extra_objects):
        if self._legacy:
            return self._legacy_signature_hash_input_get(*extra_objects)

        e = j.data.rivine.encoder_sia_get()

        # encode the transaction version
        e.add_byte(self.version)

        # encode extra objects if exists
        if extra_objects:
            e.add_all(*extra_objects)

        # encode the number of coins inputs
        e.add(len(self.coin_inputs))
        # encode coin inputs parent_ids
        for ci in self.coin_inputs:
            e.add(ci.parentid)

        # encode coin outputs
        e.add_slice(self.coin_outputs)

        # encode the number of blockstake inputs
        e.add(len(self.blockstake_inputs))
        # encode blockstake inputs parent_ids
        for bsi in self.blockstake_inputs:
            e.add(bsi.parentid)

        # encode blockstake outputs
        e.add_slice(self.blockstake_outputs)

        # encode miner fees
        e.add_slice(self.miner_fees)

        # encode custom data
        e.add(self.data)

        # return the encoded data
        return e.data

    def _legacy_signature_hash_input_get(self, *extra_objects):
        e = j.data.rivine.encoder_sia_get()

        # encode extra objects if exists
        if extra_objects:
            e.add_all(*extra_objects)

        # encode coin inputs
        for ci in self.coin_inputs:
            e.add_all(ci.parentid, ci.fulfillment.public_key.unlockhash)

        # encode coin outputs
        e.add(len(self.coin_outputs))
        for co in self.coin_outputs:
            e.add_all(co.value, co.condition.unlockhash)

        # encode blockstake inputs
        for bsi in self.blockstake_inputs:
            e.add_all(bsi.parentid, bsi.fulfillment.public_key.unlockhash)

        # encode blockstake outputs
        e.add(len(self.blockstake_outputs))
        for bso in self.blockstake_outputs:
            e.add_all(bso.value, bso.condition.unlockhash)

        # encode miner fees
        e.add_slice(self.miner_fees)

        # encode custom data
        e.add(self.data)

        # return the encoded data
        return e.data

    def _from_json_data_object(self, data):
        self._coin_inputs = [CoinInput.from_json(ci) for ci in data.get("coininputs", []) or []]
        self._coin_outputs = [CoinOutput.from_json(co) for co in data.get("coinoutputs", []) or []]
        self._blockstake_inputs = [BlockstakeInput.from_json(bsi) for bsi in data.get("blockstakeinputs", []) or []]
        self._blockstake_outputs = [BlockstakeOutput.from_json(bso) for bso in data.get("blockstakeoutputs", []) or []]
        self._miner_fees = [Currency.from_json(fee) for fee in data.get("minerfees", []) or []]
        self._data = BinaryData.from_json(data.get("arbitrarydata", None) or "", strencoding="base64")

    def _json_data_object(self):
        obj = {
            "coininputs": [ci.json() for ci in self._coin_inputs],
            "coinoutputs": [co.json() for co in self._coin_outputs],
            "blockstakeinputs": [bsi.json() for bsi in self._blockstake_inputs],
            "blockstakeoutputs": [bso.json() for bso in self._blockstake_outputs],
            "minerfees": [fee.json() for fee in self._miner_fees],
            "arbitrarydata": self.data.json(),
        }
        keys = list(obj.keys())
        for key in keys:
            if not obj[key]:
                del obj[key]
        return obj

    @property
    def _coin_outputid_specifier(self):
        if self._legacy:
            return b"coin output\0\0\0\0"
        return super()._coin_outputid_specifier

    @property
    def _blockstake_outputid_specifier(self):
        if self._legacy:
            return b"blstake output\0"
        return super()._blockstake_outputid_specifier

    def binary_encode(self):
        """
        Binary encoding of a Transaction,
        overriden to specify the version correctly
        """
        if self._legacy:
            return bytearray([TransactionVersion.LEGACY]) + self._binary_encode_data()
        encoder = j.data.rivine.encoder_sia_get()
        encoder.add_array(bytearray([TransactionVersion.STANDARD]))
        encoder.add_slice(self._binary_encode_data())
        return encoder.data

    def _binary_encode_data(self):
        if not self._legacy:
            return super()._binary_encode_data()
        # encoding was slightly different in legacy transactions (v0)
        # (NOTE: we only support the subset of v0 transactions that are actually active on the tfchain network)
        encoder = j.data.rivine.encoder_sia_get()
        # > encode coin inputs
        encoder.add_int(len(self.coin_inputs))
        for ci in self.coin_inputs:
            encoder.add(ci.parentid)
            encoder.add_array(bytearray([1]))  # FulfillmentTypeSingleSignature
            sub_encoder = j.data.rivine.encoder_sia_get()
            sub_encoder.add(ci.fulfillment.public_key)
            encoder.add_slice(sub_encoder.data)
            encoder.add(ci.fulfillment.signature)
        # > encode coin outputs
        encoder.add_int(len(self.coin_outputs))
        for co in self.coin_outputs:
            encoder.add_all(co.value, co.condition.unlockhash)
        # > encode block stake inputs
        encoder.add_int(len(self._blockstake_inputs))
        for bsi in self._blockstake_inputs:
            encoder.add(bsi.parentid)
            encoder.add_array(bytearray([1]))  # FulfillmentTypeSingleSignature
            sub_encoder = j.data.rivine.encoder_sia_get()
            sub_encoder.add(bsi.fulfillment.public_key)
            encoder.add_slice(sub_encoder.data)
            encoder.add(bsi.fulfillment.signature)
        # > encode block stake outputs
        encoder.add_int(len(self._blockstake_outputs))
        for bso in self.blockstake_outputs:
            encoder.add_all(bso.value, bso.condition.unlockhash)
        # > encode miner fees and arbitrary data
        encoder.add_all(self.miner_fees, self.data)
        return encoder.data
