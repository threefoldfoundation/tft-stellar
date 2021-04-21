##ERRORS


class IntegerOutOfRange(Exception):
    """
    IntegerOutOfRange error
    """


class SliceLengthOutOfRange(Exception):
    """
    SliceLengthOutOfRange error
    """


_INT_1BYTE_UPPERLIMIT = pow(2, 8) - 1
_INT_2BYTE_UPPERLIMIT = pow(2, 16) - 1
_INT_3BYTE_UPPERLIMIT = pow(2, 24) - 1
_INT_4BYTE_UPPERLIMIT = pow(2, 32) - 1
_INT_8BYTE_UPPERLIMIT = pow(2, 64) - 1

from abc import ABC, abstractmethod


class RivineBinaryObjectEncoderBase(ABC):
    @abstractmethod
    def rivine_binary_encode(self, encoder):
        """
        rivine_binary_encode encodes this object as a byte-slice,
        using the primitive encoding functions provided by the RivineBinaryEncoder module,
        resulting in a custom and/or complex byteslice,
        encoded according to the rivbin encoding specification.
        """
        pass


class RivineBinaryEncoder(object):
    """
    Module implementing the rivbin binary encoding,
    for the purposes of creating signatures only.

    Decoding of rivbin-encoded data is not supported,
    and is out of scope for the rivine binary encoder Module.

    official specification can be found at
    https://github.com/threefoldtech/rivine/blob/7c87733e250d0e195c87119208fe7ba15e762e4b/doc/encoding/RivineEncoding.md
    """

    def __init__(self, **kwargs):
        self._data = bytearray()

    @property
    def data(self):
        return self._data

    def reset(self):
        self._data = bytearray()

    def add(self, value):
        """
        Add a value, after encoding it as specified by the rivbin encoding specification,
        automatically matching the value's type with a matching rivbin type.

        Use a specific encoding function if you want to make sure you
        encode in a specific way.

        NOTE: an integer will always be encoded as an 64-bit integer,
              use a specific add_intx method if this is not desireable.

        @param value: the value to be rivbin-encoded
        """

        # if the value implements the RivineBinaryObjectEncoderBase class,
        # we ignore the underlying type and use the custom-defined logic
        # as provided by the RivineBinaryObjectEncoder.
        if isinstance(value, RivineBinaryObjectEncoderBase):
            value.rivine_binary_encode(encoder=self)
            return

        # try to rivbin-encode the value based on its python type
        if isinstance(value, bool):
            if value:
                self._data += bytearray([1])
            else:
                self._data += bytearray([0])
        elif isinstance(value, int):
            self.add_int64(value)
        else:
            # try to rivbin-encode the value as a slice
            try:
                self.add_slice(value)
                return
            except TypeError:
                pass
            raise Exception("cannot rivbin-encode value with unsupported type {}".format(type(value)))

    def _check_int_type(self, value, limit):
        if not isinstance(value, int):
            raise Exception("value is not an integer")
        if value < 0:
            raise IntegerOutOfRange("integer {} is out of lower range of 0".format(value))
        if value > limit:
            raise IntegerOutOfRange("integer {} is out of upper range of {}".format(value, limit))

    def add_int8(self, value):
        """
        Encode an uin8/int8 as a single byte, using little-endianness,
        as specified by the rivbin encoding specification.

        @param value: int value that fits in a single byte
        """
        self._check_int_type(value, _INT_1BYTE_UPPERLIMIT)
        self._data += value.to_bytes(1, byteorder="little")

    def add_int16(self, value):
        """
        Encode an uin16/int16 as two bytes, using little-endianness,
        as specified by the rivbin encoding specification.

        @param value: int value that fits in two bytes
        """
        self._check_int_type(value, _INT_2BYTE_UPPERLIMIT)
        self._data += value.to_bytes(2, byteorder="little")

    def add_int24(self, value):
        """
        Encode an uin24/int24 as three bytes, using little-endianness,
        as specified by the rivbin encoding specification.

        @param value: int value that fits in three bytes
        """
        self._check_int_type(value, _INT_3BYTE_UPPERLIMIT)
        self._data += value.to_bytes(3, byteorder="little")

    def add_int32(self, value):
        """
        Encode an uin32/int32 as four bytes, using little-endianness,
        as specified by the rivbin encoding specification.

        @param value: int value that fits in four bytes
        """
        self._check_int_type(value, _INT_4BYTE_UPPERLIMIT)
        self._data += value.to_bytes(4, byteorder="little")

    def add_int64(self, value):
        """
        Encode an uint64/int64 as three bytes, using little-endianness,
        as specified by the rivbin encoding specification.

        @param value: int value that fits in eight bytes
        """
        self._check_int_type(value, _INT_8BYTE_UPPERLIMIT)
        self._data += value.to_bytes(8, byteorder="little")

    def add_array(self, value):
        """
        Encode an iterateble value as an array,
        as specified by the rivbin encoding specification.

        @param value: the iterateble object to be rivbin-encoded as an array
        """
        if isinstance(value, str):
            self._data += value.encode("utf-8")
        elif isinstance(value, (bytes, bytearray)):
            self._data += value
        else:
            try:
                for element in value:
                    self.add(element)
            except TypeError:
                raise Exception("value cannot be encoded as an array")

    def add_slice(self, value):
        """
        Encode an iterateble value as a slice,
        as specified by the rivbin encoding specification.

        @param value: the iterateble object to be rivbin-encoded as a slice
        """
        if isinstance(value, str):
            self._add_slice_length(len(value))
            self._data += value.encode("utf-8")
        elif isinstance(value, (bytes, bytearray)):
            self._add_slice_length(len(value))
            self._data += value
        else:
            length = 0
            for _ in value:
                length += 1
            self._add_slice_length(length)
            self.add_array(value)

    def _add_slice_length(self, length):
        """
        Encodes the length of the slice
        """
        if length < pow(2, 7):
            self.add_int8(length << 1)
        elif length < pow(2, 14):
            self.add_int16(1 | length << 2)
        elif length < pow(2, 21):
            self.add_int24(3 | length << 3)
        elif length < pow(2, 29):
            self.add_int32(7 | length << 3)
        else:
            raise SliceLengthOutOfRange("slice length {} is out of range".format(length))

    def add_byte(self, value):
        """
        Add an encoded iterateble value as a single byte.

        @param value: the value to be added as a single byte
        """
        if isinstance(value, int):
            self.add_int8(int(value))
        else:
            if isinstance(value, str):
                value = value.encode("utf-8")
            elif not isinstance(value, (bytes, bytearray)):
                raise Exception("value of type {} cannot be added as a single byte".format(type(value)))
            if len(value) != 1:
                raise j.exceptions.Value(
                    "a single byte has to be accepted, amount of bytes given: {}".format(len(value))
                )
            self._data += value

    def add_all(self, *values):
        """
        Encode values, one by one, as specified by the rivbin encoding specification,
        automatically matching each value's type with a matching rivbin type.

        Each value is encoded one after another within a single bytearray.

        @param values: the values to be rivbin-encoded
        """
        for value in values:
            self.add(value)
