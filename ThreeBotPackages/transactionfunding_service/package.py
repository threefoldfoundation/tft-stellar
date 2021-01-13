import os
import sys
import toml
from decimal import Decimal

import gevent
import gevent.queue

from jumpscale.loader import j

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/sals/")
from transactionfunding_sal import (
    ASSET_ISSUERS,
    ensure_slavewallets,
    start_funding_loop,
    set_wallet_name,
    stop_funding_loop,
)


class transactionfunding_service:
    def install(self, **kwargs):
        wallet_name = kwargs.get("wallet", "txfundingwallet")
        set_wallet_name(wallet_name)
        main_wallet = None
        if wallet_name not in j.clients.stellar.list_all():
            secret = kwargs.get("secret", None)
            if not secret:
                secret = os.environ.get("TXFUNDING_WALLET_SECRET", None)
            network = kwargs.get("network", None)

            if not network:
                network = os.environ.get("TFT_SERVICES_NETWORK", "TEST")
            if network:
                main_wallet = j.clients.stellar.new(wallet_name, secret=secret, network=network)
                if not secret:
                    if network == "TEST":
                        main_wallet.activate_through_friendbot()
                        main_wallet.save()

        # make sure the trustlines exist for the main wallet
        if wallet_name in j.clients.stellar.list_all() and main_wallet:
            main_wallet.add_known_trustline("TFT")
            main_wallet.add_known_trustline("TFTA")

        nr_of_slaves = kwargs.get("slaves", 30)
        ensure_slavewallets(nr_of_slaves)

        start_funding_loop()

    def start(self, **kwargs):
        self.install(**kwargs)

    def uninstall(self):
        """Called when package is deleted
        """
        if "default_443" in j.sals.nginx.main.websites.list_all():
            j.sals.nginx.main.websites.default_443.locations.delete("transactionfunding_root_proxy")

        if "default_80" in j.sals.nginx.main.websites.list_all():
            j.sals.nginx.main.websites.default_80.locations.delete("transactionfunding_root_proxy")

    def stop(self):
        stop_funding_loop()
