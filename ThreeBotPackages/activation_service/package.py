import os
import sys
import toml

import gevent

from jumpscale.loader import j

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/sals/")
from activation_sal import create_gevent_pool, set_wallet_name


class activation_service:
    def install(self, **kwargs):
        wallet_name = kwargs.get("wallet", "activation_wallet")
        set_wallet_name(wallet_name)
        if wallet_name not in j.clients.stellar.list_all():
            secret = kwargs.get("secret", None)
            network = kwargs.get("network", "TEST")
            wallet = j.clients.stellar.new(wallet_name, secret=secret, network=network)
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

        # Configure server domain (passed as kwargs if not, will be the default domain in package.toml)
        if "domain" in kwargs:
            domain = kwargs.get("domain")
            toml_config = toml.load(j.sals.fs.join_paths(j.sals.fs.dirname(__file__), "package.toml"))
            package_name = toml_config["name"]
            server_name = toml_config["servers"][0]["name"]

            j.sals.nginx.main.websites.get(f"{package_name}_{server_name}_443").domain = domain
            j.sals.nginx.main.websites.get(f"{package_name}_{server_name}_443").configure()
            j.sals.nginx.main.websites.get(f"{package_name}_{server_name}_80").domain = domain
            j.sals.nginx.main.websites.get(f"{package_name}_{server_name}_80").configure()

        j.sals.nginx.main.websites.default_443.configure()
        j.sals.nginx.main.websites.default_80.configure()

        create_gevent_pool()

    def start(self, **kwargs):
        self.install(**kwargs)

    def uninstall(self):
        """Called when package is deleted
        """
        j.sals.nginx.main.websites.default_443.locations.delete("activation_root_proxy")
        j.sals.nginx.main.websites.default_80.locations.delete("activation_root_proxy")