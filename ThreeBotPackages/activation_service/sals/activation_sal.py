from jumpscale.loader import j
import gevent

pool = None
WALLET = None


def create_gevent_pool():
    global pool
    pool = gevent.pool.Pool(1)


def _activate_account(address):
    WALLET.activate_account(address, starting_balance="3.6")


def activate_account(address):
    pool.apply(_activate_account, args=(address,))


def set_wallet(wallet):
    global WALLET
    WALLET = wallet

def get_wallet():
    return WALLET


 