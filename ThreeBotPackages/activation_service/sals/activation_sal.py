from jumpscale.loader import j
import gevent

pool = None
WALLET_NAME = "activation_wallet"


def create_gevent_pool():
    global pool
    pool = gevent.pool.Pool(1)


def _activate_account(address):
    j.clients.stellar.get(WALLET_NAME).activate_account(address, starting_balance="3.6")


def activate_account(address):
    pool.apply(_activate_account, args=(address,))


def set_wallet_name(wallet_name):
    global WALLET_NAME
    WALLET_NAME = wallet_name

