import os
import sys
import toml

import gevent

from jumpscale.loader import j

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/sals/")
from tfchainmigration_sal import create_gevent_pools, set_wallet


class tfchainmigration_service:
    def install(self, **kwargs):
        wallet = None
        wallet_name = kwargs.get("wallet", "converter_wallet")
        j.logger.info(f"using {wallet_name} for the migration service")
        if wallet_name in j.clients.stellar.list_all():
            j.logger.info(f"wallet {wallet_name} already exists, reusing it")
            wallet = j.clients.stellar.get(wallet_name)
        else:
            secret = kwargs.get("secret", None)
            if not secret:
                secret = os.environ.get("MIGRATION_WALLET_SECRET", None)
            network = kwargs.get("network", None)
            if not network:
                network = os.environ.get("TFT_SERVICES_NETWORK", None)
            if network:
                wallet = j.clients.stellar.new(wallet_name, secret=secret, network=network)
            if not secret and network == "TEST":
               wallet.activate_through_friendbot()

        set_wallet(wallet)

        create_gevent_pools()

    def start(self, **kwargs):
        self.install(**kwargs)
