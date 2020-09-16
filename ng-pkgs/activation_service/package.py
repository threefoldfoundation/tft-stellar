from jumpscale.loader import j
import gevent

class activation:
    def install(self, **kwargs):
        if "activation_wallet" not in j.clients.stellar.list_all():
            secret = kwargs.get("secret", None)
            network = kwargs.get("network", "TEST")
            wallet = j.clients.stellar.new("activation_wallet", secret=secret, network=network)
            if not secret:
                if network == "TEST":
                    wallet.activate_through_friendbot()
                else:
                    wallet.activate_through_threefold_service()
            wallet.save()



        location_actors_443 = j.sals.nginx.main.websites.default_443.locations.get(name="activation_actors")
        location_actors_443.is_auth = False
        location_actors_443.is_admin = False
        location_actors_443.save()

        location_actors_80 = j.sals.nginx.main.websites.default_80.locations.get(name="activation_actors")
        location_actors_80.is_auth = False
        location_actors_80.is_admin = False
        location_actors_80.save()

        j.sals.nginx.main.websites.default_443.configure()
        j.sals.nginx.main.websites.default_80.configure()

    def start(self):
        self.install()

    def uninstall(self):
        """Called when package is deleted
        """
        j.sals.nginx.main.websites.default_443.locations.delete("activation_root_proxy")
        j.sals.nginx.main.websites.default_80.locations.delete("activation_root_proxy")

        self.pool = gevent.pool.Pool(1)

    def _activate_account(self, address):
        j.clients.stellar.activation_wallet.activate_account(address, starting_balance="3.6")

    def activate_account(self, address):
        self.pool.apply(self._activate_account, args=(address,))