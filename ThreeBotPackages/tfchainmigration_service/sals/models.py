import ipaddress
from datetime import datetime
from enum import Enum

from jumpscale.core.base import Base, fields


class ConvertedAddress(Base):
    stellaraddress = fields.String()
