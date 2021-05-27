from jumpscale.loader import j
import gevent

WALLET = None


def set_wallet(wallet):
    global WALLET
    WALLET = wallet


def get_wallet():
    return WALLET
