from abc import abstractmethod, abstractclassmethod
from .rivine.RivineBinaryEncoder import RivineBinaryObjectEncoderBase
from .rivine.SiaBinaryEncoder import SiaBinaryObjectEncoderBase


class BaseDataTypeClass(SiaBinaryObjectEncoderBase, RivineBinaryObjectEncoderBase):
    """
    Base type defines the type all TFChain data types inheret from.
    """

    @abstractclassmethod
    def from_json(cls, obj):
        pass

    @abstractmethod
    def json(self):
        pass
