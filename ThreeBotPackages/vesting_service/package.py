import os
import sys
import os
import toml

from jumpscale.loader import j

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/sals/")
from vesting_sal import set_wallet, set_unvesting_transactions


class vesting_service:
    def install(self, **kwargs):
        wallet = None
        wallet_name = kwargs.get("wallet", "vesting_wallet")
        j.logger.info(f"using {wallet_name} for the vesting service")
        network = kwargs.get("network", None)
        if not network:
            network = os.environ.get("TFT_SERVICES_NETWORK", "TEST")
        if wallet_name in j.clients.stellar.list_all():
            j.logger.info(f"wallet {wallet_name} already exists, reusing it")
            wallet = j.clients.stellar.get(wallet_name)
        else:
            secret = kwargs.get("secret", None)
            if not secret:
                secret = os.environ.get("VESTING_WALLET_SECRET", None)
            if network:
                wallet = j.clients.stellar.new(wallet_name, secret=secret, network=network)
            if not secret and network == "TEST":
                wallet.activate_through_friendbot()

        set_wallet(wallet)

        unvesting_transactions = {}
        with open(current_full_path + "/signed_unvesting_transactions.txt", "r") as txfile:
            for line in txfile:
                vesting_account, unvesting_transaction = line.split(" ")
                unvesting_transactions[vesting_account] = unvesting_transaction.strip()
        set_unvesting_transactions(unvesting_transactions)

    def start(self, **kwargs):
        self.install(**kwargs)
