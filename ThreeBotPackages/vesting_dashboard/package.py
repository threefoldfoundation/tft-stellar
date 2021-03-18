from jumpscale.loader import j

wallet_name = "vesting_temp_wallet"


class vesting_dashboard:
    def install(self, **kwargs):
        """Called when package is added"""
        wallet = None
        wallet_name = "vesting_temp_wallet"  # Only to be used to check balance of other wallets, no need to activate
        if "vesting_temp_wallet" not in j.clients.stellar.list_all():
            wallet_network = kwargs.get("wallet_network", "STD")
            wallet = j.clients.stellar.get(wallet_name)
            wallet.network = wallet_network
            wallet.save()

    def start(self, **kwargs):
        self.install(**kwargs)

    def uninstall(self):
        """Called when package is deleted"""
        j.sals.nginx.main.websites.default_443.locations.delete("vesting_dashboard_root_proxy")
        j.sals.nginx.main.websites.default_80.locations.delete("vesting_dashboard_root_proxy")
