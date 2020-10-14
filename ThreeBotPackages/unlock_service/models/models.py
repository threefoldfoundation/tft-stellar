import ipaddress
from datetime import datetime
from enum import Enum

from jumpscale.core.base import Base, fields


class UnlockhashTransaction(Base):
    unlockhash = fields.String()

    transaction_xdr = fields.String()
