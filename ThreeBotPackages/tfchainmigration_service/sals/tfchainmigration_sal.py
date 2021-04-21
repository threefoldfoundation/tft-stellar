import gevent

from jumpscale.core.base import StoredFactory,Base, fields
from jumpscale.loader import j


class ConvertedAddress(Base):
    stellaraddress = fields.String()

# pool = None
activation_pool = None
tft_issuing_pool = None
tfta_issuing_pool = None
db_pool = None

WALLET = None

CONVERTED_ADDRESS_MODEL = StoredFactory(ConvertedAddress)
CONVERTED_ADDRESS_MODEL.always_reload = True


def create_gevent_pools():
    global activation_pool, tft_issuing_pool, tfta_issuing_pool, db_pool
    activation_pool = gevent.pool.Pool(1)
    tft_issuing_pool = gevent.pool.Pool(1)
    tfta_issuing_pool = gevent.pool.Pool(1)
    db_pool = gevent.pool.Pool(1)


def _activate_account(address):
    get_wallet().activate_account(address, starting_balance="3.6")


def activate_account(address):
    activation_pool.apply(_activate_account, args=(address,))


def set_wallet(wallet):
    global WALLET
    WALLET = wallet


def get_wallet():
    return WALLET