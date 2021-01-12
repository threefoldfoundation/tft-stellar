import os
import sys
import os
import toml

import gevent

from jumpscale.loader import j

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/sals/")
from activation_sal import create_gevent_pool, set_wallet


class activation_service:
    def install(self, **kwargs):
        wallet_name = kwargs.get("wallet", "activation_wallet")
        if wallet_name in j.clients.stellar.list_all():
            wallet = j.clients.stellar.get(wallet_name)
        else:
            secret = kwargs.get("secret", None)
            if not secret:
                secret = os.environ.get("ACTIVATION_WALLET_SECRET", None)
            network = kwargs.get("network", None)
            if not network:
                network = os.environ.get("TFT_SERVICES_NETWORK", "TEST")
            wallet = j.clients.stellar.new(wallet_name, secret=secret, network=network)
            if not secret:
                if network == "TEST":
                    wallet.activate_through_friendbot()

        set_wallet(wallet)

        create_gevent_pool()

    def start(self, **kwargs):
        self.install(**kwargs)

    def uninstall(self):
        """Called when package is deleted"""
        j.sals.nginx.main.websites.default_443.locations.delete("activation_root_proxy")
        j.sals.nginx.main.websites.default_80.locations.delete("activation_root_proxy")
