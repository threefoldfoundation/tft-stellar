from jumpscale.core.base import Base, fields
from jumpscale.loader import j


class VestingEntry(Base):
    username = fields.String()
    owner_address = fields.String()
    vesting_address = fields.String()