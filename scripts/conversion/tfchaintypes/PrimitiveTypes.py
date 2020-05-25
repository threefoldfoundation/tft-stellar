
from enum import IntEnum

from .BaseDataType import BaseDataTypeClass


class BinaryData(BaseDataTypeClass):
    """
    BinaryData is the data type used for any binary data used in tfchain.
    """

    def __init__(self, value=None, fixed_size=None, strencoding=None):
        # define string encoding
        if strencoding is not None and not isinstance(strencoding, str):
            raise Exception("strencoding should be None or a str, not be of type {}".format(strencoding))
        if strencoding is None or strencoding.lower().strip() == "hex":
            self._from_str = lambda s: bytearray.fromhex(s)
            self._to_str = lambda value: value.hex()
        elif strencoding.lower().strip() == "base64":
            self._from_str = lambda s: bytearray(j.data.serializers.base64.decode(s))
            self._to_str = lambda value: j.data.serializers.base64.dumps(value)
        elif strencoding.lower().strip() == "hexprefix":
            self._from_str = lambda s: bytearray.fromhex(s[2:] if (s.startswith("0x") or s.startswith("0X")) else s)
            self._to_str = lambda value: "0x" + value.hex()
        else:
            raise j.exceptions.Value("{} is not a valid string encoding".format(strencoding))
        self._strencoding = strencoding

        # define fixed size
        if fixed_size is not None:
            if not isinstance(fixed_size, int):
                raise Exception("fixed size should be None or int, not be of type {}".format(type(fixed_size)))
            if fixed_size < 0:
                raise Exception("fixed size should be at least 0, {} is not allowed".format(fixed_size))
        if fixed_size != 0:
            self._fixed_size = fixed_size
        else:
            self._fixed_size = None  # for now use no fixed size

        # define the value (finally)
        self._value = None
        self.value = value

        if fixed_size == 0:
            # define the fixed size now, if the fixed_size was 0
            self._fixed_size = len(self.value)  # based on the binary length of the value

    @classmethod
    def from_json(cls, obj, fixed_size=None, strencoding=None):
        if obj is not None and not isinstance(obj, str):
            raise Exception("binary data is expected to be an encoded string when part of a JSON object")
        if obj == "":
            obj = None
        return cls(value=obj, fixed_size=fixed_size, strencoding=strencoding)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # normalize the value
        if isinstance(value, BinaryData):
            value = value.value
        elif value is None:
            value = bytearray()
        elif isinstance(value, str):
            value = self._from_str(value)
        elif isinstance(value, bytes):
            value = bytearray(value)
        elif not isinstance(value, bytearray):
            raise j.exceptions.Value(
                "binary data can only be set to a BinaryData, str, bytes or bytearray, not {}".format(type(value))
            )
        # if fixed size, check this now
        lvalue = len(value)
        if self._fixed_size is not None and lvalue != 0 and lvalue != self._fixed_size:
            raise j.exceptions.Value(
                "binary data was expected to be of fixed size {}, length {} is not allowed".format(
                    self._fixed_size, len(value)
                )
            )
        # all good, assign the bytearray value
        self._value = value

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return self._to_str(self._value)

    def __repr__(self):
        return self.__str__()

    def json(self):
        return self.__str__()

    def __eq__(self, other):
        other = self._op_other_as_binary_data(other)
        return self.value == other.value

    def __ne__(self, other):
        other = self._op_other_as_binary_data(other)
        return self.value != other.value

    def _op_other_as_binary_data(self, other):
        if isinstance(other, (str, bytes, bytearray)):
            other = BinaryData(value=other, fixed_size=self._fixed_size, strencoding=self._strencoding)
        elif not isinstance(other, BinaryData):
            raise Exception("Binary data of type {} is not supported".format(type(other)))
        if self._fixed_size != other._fixed_size:
            raise Exception(
                "Cannot compare binary data with different fixed size: self({}) != other({})".format(
                    self._fixed_size, other._fixed_size
                )
            )
        if self._strencoding != other._strencoding:
            raise Exception(
                "Cannot compare binary data with different strencoding: self({}) != other({})".format(
                    self._strencoding, other._strencoding
                )
            )
        return other

    def __hash__(self):
        return hash(str(self))

    def sia_binary_encode(self, encoder):
        """
        Encode this binary data according to the Sia Binary Encoding format.
        Either encoded as a slice or an array, depending on whether or not it is fixed sized.
        """
        if self._fixed_size is None:
            encoder.add_slice(self._value)
        else:
            encoder.add_array(self._value)

    def rivine_binary_encode(self, encoder):
        """
        Encode this binary data according to the Rivine Binary Encoding format.
        Either encoded as a slice or an array, depending on whether or not it is fixed sized.
        """
        if self._fixed_size is None:
            encoder.add_slice(self._value)
        else:
            encoder.add_array(self._value)


class Hash(BinaryData):
    SIZE = 32

    """
    TFChain Hash Object, a special type of BinaryData
    """

    def __init__(self, value=None):
        super().__init__(value, fixed_size=Hash.SIZE, strencoding="hex")

    @classmethod
    def from_json(cls, obj):
        if obj is not None and not isinstance(obj, str):
            raise Exception(
                "hash is expected to be an encoded string when part of a JSON object, not {}".format(type(obj))
            )
        if obj == "":
            obj = None
        return cls(value=obj)

    def __str__(self):
        s = super().__str__()
        if not s:
            return "0" * (Hash.SIZE * 2)
        return s


from math import floor
from decimal import Decimal


class Currency(BaseDataTypeClass):
    """
    TFChain Currency Object.
    """

    def __init__(self, value=None):
        self._value = None
        self.value = value

    @classmethod
    def from_json(cls, obj):
        if obj is not None and not isinstance(obj, str):
            raise Exception(
                "currency is expected to be a string when part of a JSON object, not type {}".format(type(obj))
            )
        if obj == "":
            obj = None
        c = cls()
        c.value = Decimal(obj) * Decimal("0.000000001")
        return c

    @property
    def value(self):
        if self._value is None:
            return Decimal()
        return self._value

    @value.setter
    def value(self, value):
        if value is None:
            self._value = None
            return
        if isinstance(value, Currency):
            self._value = value.value
            return
        if isinstance(value, (int, str, Decimal)):
            if isinstance(value, str):
                value = value.upper().strip()
                if len(value) >= 4 and value[-3:] == "TFT":
                    value = value[:-3].rstrip()
            d = Decimal(value)
            sign, _, exp = d.as_tuple()
            if exp < -9:
                raise  Exception("CurrencyPrecisionOverflow")
            if sign != 0:
                raise Exception("Negative currency")
            self._value = d
            return
        raise Exception("cannot set value of type {} as Currency (invalid type)".format(type(value)))

    # operator overloading to allow currencies to be summed
    def __add__(self, other):
        other = Currency._op_other_as_currency(other)
        value = self.value + other.value
        return Currency(value=value)

    __radd__ = __add__

    def __iadd__(self, other):
        other = Currency._op_other_as_currency(other)
        self.value += other.value
        return self

    # operator overloading to allow currencies to be multiplied
    def __mul__(self, other):
        other = Currency._op_other_as_currency(other)
        value = self.value * other.value
        return Currency(value=value)

    __rmul__ = __mul__

    def __imul__(self, other):
        other = Currency._op_other_as_currency(other)
        self.value *= other.value
        return self

    # operator overloading to allow currencies to be subtracted
    def __sub__(self, other):
        other = Currency._op_other_as_currency(other)
        value = self.value - other.value
        return Currency(value=value)

    __rsub__ = __sub__

    def __isub__(self, other):
        other = Currency._op_other_as_currency(other)
        self.value -= other.value
        return self

    # operator overloading to allow currencies to be compared
    def __lt__(self, other):
        other = Currency._op_other_as_currency(other)
        return self.value < other.value

    def __le__(self, other):
        other = Currency._op_other_as_currency(other)
        return self.value <= other.value

    def __eq__(self, other):
        other = Currency._op_other_as_currency(other)
        return self.value == other.value

    def __ne__(self, other):
        other = Currency._op_other_as_currency(other)
        return self.value != other.value

    def __gt__(self, other):
        other = Currency._op_other_as_currency(other)
        return self.value > other.value

    def __ge__(self, other):
        other = Currency._op_other_as_currency(other)
        return self.value >= other.value

    @staticmethod
    def _op_other_as_currency(other):
        if isinstance(other, (int, str)):
            other = Currency(value=other)
        elif isinstance(other, float):
            other = Currency(value=Decimal(str(other)))
        elif not isinstance(other, Currency):
            raise j.exceptions.Value("currency of type {} is not supported".format(type(other)))
        return other

    # allow our currency to be turned into an int
    def __int__(self):
        s = "{:.9f}".format(self.value).replace(".", "")
        return int(s)

    def __str__(self):
        return self.str()

    def str(self, with_unit=False):
        """
        Turn this Currency value into a str TFT unit-based value,
        optionally with the currency notation.

        @param with_unit: include the TFT currency suffix unit with the str
        """
        s = "{:.9f}".format(self.value)
        s = s.rstrip("0 ")
        if s[-1] == ".":
            s = s[:-1]
        if len(s) == 0:
            s = "0"
        if with_unit:
            s += " TFT"
        return s

    def __repr__(self):
        return self.str(with_unit=True)

    def json(self):
        return str(int(self))

    def sia_binary_encode(self, encoder):
        """
        Encode this currency according to the Sia Binary Encoding format.
        """
        value = int(self)
        nbytes, rem = divmod(value.bit_length(), 8)
        if rem:
            nbytes += 1
        encoder.add_int(nbytes)
        encoder.add_array(value.to_bytes(nbytes, byteorder="big"))

    def rivine_binary_encode(self, encoder):
        """
        Encode this currency according to the Rivine Binary Encoding format.
        """
        value = int(self)
        nbytes, rem = divmod(value.bit_length(), 8)
        if rem:
            nbytes += 1
        encoder.add_slice(value.to_bytes(nbytes, byteorder="big"))


class Blockstake(BaseDataTypeClass):
    """
    TFChain Blockstake Object.
    """

    def __init__(self, value=0):
        self._value = 0
        self.value = value

    @classmethod
    def from_json(cls, obj):
        if obj is not None and not isinstance(obj, str):
            raise j.exceptions.Value(
                "block stake is expected to be a string when part of a JSON object, not type {}".format(type(obj))
            )
        if obj == "":
            obj = None
        return cls(value=obj)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value is None:
            self._value = 0
            return
        if isinstance(value, Currency):
            self._value = value.value
            return
        if isinstance(value, str):
            value = int(value)
        elif not isinstance(value, int):
            # float values are not allowed as our precision is high enough that
            # rounding errors can occur
            raise j.exceptions.Value(
                "block stake can only be set to a str or int value, not type {}".format(type(value))
            )
        else:
            value = int(value)
        if value < 0:
            raise j.exceptions.Value("block stake cannot have a negative value")
        self._value = value

    # allow our block stake to be turned into an int
    def __int__(self):
        return self.value

    def __str__(self):
        return str(self._value)

    __repr__ = __str__
    json = __str__

    def sia_binary_encode(self, encoder):
        """
        Encode this block stake (==Currency) according to the Sia Binary Encoding format.
        """
        nbytes, rem = divmod(self._value.bit_length(), 8)
        if rem:
            nbytes += 1
        encoder.add_int(nbytes)
        encoder.add_array(self._value.to_bytes(nbytes, byteorder="big"))

    def rivine_binary_encode(self, encoder):
        """
        Encode this block stake (==Currency) according to the Rivine Binary Encoding format.
        """
        nbytes, rem = divmod(self._value.bit_length(), 8)
        if rem:
            nbytes += 1
        encoder.add_slice(self._value.to_bytes(nbytes, byteorder="big"))
