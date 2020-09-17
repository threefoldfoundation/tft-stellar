from jumpscale.loader import j
import gevent


pool = None


def create_gevent_pool():
    global pool
    pool = gevent.pool.Pool(1)


def _activate_account(self, address):
    j.clients.stellar.activation_wallet.activate_account(address, starting_balance="3.6")


def activate_account(self, address):
    pool.apply(self._activate_account, args=(address,))

