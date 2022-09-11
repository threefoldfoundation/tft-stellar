import gevent

from jumpscale.core.base import StoredFactory,Base, fields
from jumpscale.loader import j


activation_pool = None

WALLET = None


def create_gevent_pools():
    global activation_pool, issuing_pool, db_pool
    activation_pool = gevent.pool.Pool(1)


def _activate_account(address):
    get_wallet().activate_account(address, starting_balance="3.6")


def activate_account(address):
    activation_pool.apply(_activate_account, args=(address,))

def set_wallet(wallet):
    global WALLET
    WALLET = wallet


def get_wallet():
    return WALLET