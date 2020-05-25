from .RivineBinaryEncoder import RivineBinaryEncoder, RivineBinaryObjectEncoderBase
from .SiaBinaryEncoder import SiaBinaryEncoder, SiaBinaryObjectEncoderBase


class RivineDataFactory(object):
    """
    Tools to encode binary data for rivine
    """

    @property
    def BaseRivineObjectEncoder(self):
        return RivineBinaryObjectEncoderBase

    @property
    def BaseSiaObjectEncoder(self):
        return SiaBinaryObjectEncoderBase

    @staticmethod
    def encoder_rivine_get():
        return RivineBinaryEncoder()

    @staticmethod
    def encoder_sia_get():
        return SiaBinaryEncoder()

    @staticmethod
    def rivine_encode(*values):
        e = RivineDataFactory.encoder_rivine_get()
        e.add_all(*values)
        return e.data

    @staticmethod
    def sia_encode(*values):
        e = RivineDataFactory.encoder_sia_get()
        e.add_all(*values)
        return e.data
