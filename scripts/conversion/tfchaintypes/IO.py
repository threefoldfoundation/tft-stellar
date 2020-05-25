from .BaseDataType import BaseDataTypeClass

from .PrimitiveTypes import BinaryData, Hash, Currency, Blockstake
from .FulfillmentTypes import FulfillmentBaseClass, FulfillmentSingleSignature, FulfillmentFactory
from .ConditionTypes import ConditionBaseClass, ConditionNil, ConditionFactory


class CoinInput(BaseDataTypeClass):
    """
    CoinInput class
    """

    def __init__(self, parentid=None, fulfillment=None, parent_output=None):
        self._parent_id = None
        self.parentid = parentid
        self._fulfillment = None
        self.fulfillment = fulfillment
        # property that can be set if known, but which is not part of the actual CoinInput
        self._parent_output = None
        self.parent_output = parent_output

    @classmethod
    def from_json(cls, obj):
        return cls(
            parentid=Hash.from_json(obj["parentid"]), fulfillment=FulfillmentFactory.from_json(obj["fulfillment"])
        )

    @classmethod
    def from_coin_output(cls, co):
        if not isinstance(co, CoinOutput):
            raise Exception("invalid co parameter, expected value of type CoinOutput, not {}".format(type(co)))
        ci = cls(parentid=co.id, fulfillment=FulfillmentFactory.from_condition(co.condition))
        ci.parent_output = co
        return ci

    @property
    def parentid(self):
        return self._parent_id

    @parentid.setter
    def parentid(self, value):
        if isinstance(value, Hash):
            self._parent_id = Hash(value=value.value)
            return
        self._parent_id = Hash(value=value)

    @property
    def fulfillment(self):
        return self._fulfillment

    @fulfillment.setter
    def fulfillment(self, value):
        if value is None:
            self._fulfillment = FulfillmentSingleSignature()
            return
        if not isinstance(value, FulfillmentBaseClass):
            raise Exception(
                "cannot assign value of type {} as a  CoinInput's fulfillment (expected: FulfillmentBaseClass)".format(
                    type(value)
                )
            )
        self._fulfillment = value

    @property
    def parent_output(self):
        return self._parent_output or CoinOutput()

    @parent_output.setter
    def parent_output(self, value):
        if value is None:
            self._parent_output = None
            return
        if not isinstance(value, CoinOutput):
            raise Exception(
                "cannot assign value of type {} as a CoinInput's parent output (expected: CoinOutput)".format(
                    type(value)
                )
            )
        self._parent_output = value

    def json(self):
        return {"parentid": self._parent_id.json(), "fulfillment": self._fulfillment.json()}

    def sia_binary_encode(self, encoder):
        """
        Encode this CoinInput according to the Sia Binary Encoding format.
        """
        encoder.add_all(self._parent_id, self._fulfillment)

    def rivine_binary_encode(self, encoder):
        """
        Encode this CoinInput according to the Rivine Binary Encoding format.
        """
        encoder.add_all(self._parent_id, self._fulfillment)

    def signature_requests_new(self, input_hash_func):
        """
        Returns all signature requests that can be generated for this Coin Inputs,
        only possible if the parent (coin) output is defined and when there
        are still signatures required.
        """
        if self._parent_output is None:
            # no requestsd get created if the parent output is not set,
            # this allows for partial Tx signings
            return []
        return self._fulfillment.signature_requests_new(
            input_hash_func=input_hash_func, parent_condition=self._parent_output.condition
        )

    def is_fulfilled(self):
        """
        Returns true if this CoinInput is fulfilled.
        """
        if self._parent_output is None:
            return False
        return self._fulfillment.is_fulfilled(self._parent_output.condition)


class CoinOutput(BaseDataTypeClass):
    """
    CoinOutput class
    """

    def __init__(self, value=None, condition=None, id=None):
        self._value = None
        self.value = value
        self._condition = None
        self.condition = condition
        # property that can be set if known, but which is not part of the actual CoinOutput
        self._id = None
        self.id = id

    @classmethod
    def from_json(cls, obj):
        return cls(value=Currency.from_json(obj["value"]), condition=ConditionFactory.from_json(obj["condition"]))

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, Currency):
            self._value = value
            return
        self._value = Currency(value=value)

    @property
    def condition(self):
        return self._condition

    @condition.setter
    def condition(self, value):
        if value is None:
            self._condition = ConditionNil()
            return
        if not isinstance(value, ConditionBaseClass):
            raise Exception(
                "cannot assign value of type {} as a CoinOutput's condition (expected: ConditionBaseClass subtype)".format(
                    type(value)
                )
            )
        self._condition = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, Hash):
            self._id = Hash(value=value.value)
            return
        self._id = Hash(value=value)

    def json(self):
        return {"value": self._value.json(), "condition": self._condition.json()}

    def sia_binary_encode(self, encoder):
        """
        Encode this CoinOutput according to the Sia Binary Encoding format.
        """
        encoder.add_all(self._value, self._condition)

    def rivine_binary_encode(self, encoder):
        """
        Encode this CoinOutput according to the Rivine Binary Encoding format.
        """
        encoder.add_all(self._value, self._condition)


class BlockstakeInput(BaseDataTypeClass):
    """
    BlockstakeInput class
    """

    def __init__(self, parentid=None, fulfillment=None, parent_output=None):
        self._parent_id = None
        self.parentid = parentid
        self._fulfillment = None
        self.fulfillment = fulfillment
        # property that can be set if known, but which is not part of the actual BlockstakeInput
        self._parent_output = None
        self.parent_output = parent_output

    @classmethod
    def from_json(cls, obj):
        return cls(
            parentid=Hash.from_json(obj["parentid"]),
            fulfillment=FulfillmentFactory.from_json(obj["fulfillment"]),
        )

    @classmethod
    def from_blockstake_output(cls, bso):
        if not isinstance(bso, BlockstakeOutput):
            raise Exception("invalid type of bso {} (expected: BlockstakeOutput)".format(type(bso)))
        bsi = cls(parentid=bso.id, fulfillment=FulfillmentFactory.from_condition(bso.condition))
        bsi.parent_output = bso
        return bsi

    @property
    def parentid(self):
        return self._parent_id

    @parentid.setter
    def parentid(self, value):
        if isinstance(value, Hash):
            self._parent_id = Hash(value=value.value)
            return
        self._parent_id = Hash(value=value)

    @property
    def fulfillment(self):
        return self._fulfillment

    @fulfillment.setter
    def fulfillment(self, value):
        if value is None:
            self._fulfillment = FulfillmentSingleSignature()
            return
        if not isinstance(value, FulfillmentBaseClass):
            raise Exception(
                "cannot assign value of type {} as a BlockstakeInput's fulfillment (expected: FulfillmentBaseClass subtype)".format(
                    type(value)
                )
            )
        self._fulfillment = value

    @property
    def parent_output(self):
        return self._parent_output

    @parent_output.setter
    def parent_output(self, value):
        if value is None:
            self._parent_output = BlockstakeOutput()
            return
        if not isinstance(value, BlockstakeOutput):
            raise Exception(
                "cannot assign value of type {} as a BlockstakeInput's parent output (expected: BlockstakeOutput)".format(
                    type(value)
                )
            )
        self._parent_output = value

    def json(self):
        return {"parentid": self._parent_id.json(), "fulfillment": self._fulfillment.json()}

    def sia_binary_encode(self, encoder):
        """
        Encode this BlockstakeInput according to the Sia Binary Encoding format.
        """
        encoder.add_all(self._parent_id, self._fulfillment)

    def rivine_binary_encode(self, encoder):
        """
        Encode this BlockstakeInput according to the Rivine Binary Encoding format.
        """
        encoder.add_all(self._parent_id, self._fulfillment)

    def signature_requests_new(self, input_hash_func):
        """
        Returns all signature requests that can be generated for this Blockstake Inputs,
        only possible if the parent (blockstake) output is defined and when there
        are still signatures required.
        """
        if self._parent_output is None:
            # no requestsd get created if the parent output is not set,
            # this allows for partial Tx signings
            return []
        return self._fulfillment.signature_requests_new(
            input_hash_func=input_hash_func, parent_condition=self._parent_output.condition
        )

    def is_fulfilled(self):
        """
        Returns true if this BlockstakeInput is fulfilled.
        """
        if self._parent_output is None:
            return False
        return self._fulfillment.is_fulfilled(self._parent_output.condition)


class BlockstakeOutput(BaseDataTypeClass):
    """
    BlockstakeOutput class
    """

    def __init__(self, value=None, condition=None, id=None):
        self._value = None
        self.value = value
        self._condition = None
        self.condition = condition
        # property that can be set if known, but which is not part of the actual BlockstakeOutput
        self._id = None
        self.id = id

    @classmethod
    def from_json(cls, obj):
        return cls(
            value=Blockstake.from_json(obj["value"]),
            condition=ConditionFactory.from_json(obj["condition"]),
        )

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, Blockstake):
            self._value = value
            return
        self._value = Blockstake(value=value)

    @property
    def condition(self):
        return self._condition

    @condition.setter
    def condition(self, value):
        if value is None:
            self._condition = ConditionNil()
            return
        if not isinstance(value, ConditionBaseClass):
            raise Exception(
                "cannot assign value of type {} as a BlockstakeOutput's condition (expected: ConditionBaseClass subtype)".format(
                    type(value)
                )
            )
        self._condition = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, Hash):
            self._id = Hash(value=value.value)
            return
        self._id = Hash(value=value)

    def json(self):
        return {"value": self._value.json(), "condition": self._condition.json()}

    def sia_binary_encode(self, encoder):
        """
        Encode this BlockstakeOutput according to the Sia Binary Encoding format.
        """
        encoder.add_all(self._value, self._condition)

    def rivine_binary_encode(self, encoder):
        """
        Encode this BlockstakeOutput according to the Rivine Binary Encoding format.
        """
        encoder.add_all(self._value, self._condition)
