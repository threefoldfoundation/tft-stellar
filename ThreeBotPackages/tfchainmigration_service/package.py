import os
import sys
import toml

import gevent

from jumpscale.loader import j

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/sals/")
from activation_sal import create_gevent_pools, set_wallet_name


class tfchainmigration_service:
    def install(self, **kwargs):
        wallet_name = kwargs.get("wallet", "converter_wallet")
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

        location_actors_443 = j.sals.nginx.main.websites.default_443.locations.get(name="tfchainmigration_actors")
        location_actors_443.is_auth = False
        location_actors_443.is_admin = False
        location_actors_443.save()

        location_actors_80 = j.sals.nginx.main.websites.default_80.locations.get(name="tfchainmigration_actors")
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

        # conversion_wallet_name = self._package.install_kwargs.get("wallet", "converter")

        # self.conversion_wallet = j.clients.stellar.get(conversion_wallet_name)

        # DOMAIN = self._package.install_kwargs.get("domain", "testnet.threefoldtoken.io")
        # for port in (443, 80):
        #     website = self.openresty.get_from_port(port)
        #     website.ssl = port == 443
        #     website.domain = DOMAIN

        #     locations = website.locations.get(name=f"conversion_service_{port}_locations")

        #     include_location = locations.get_location_custom(f"conversion_service_includes_{port}")
        #     include_location.is_auth = False
        #     include_location.config = f"""
        #     location /threefoldfoundation/conversion_service {{
        #         rewrite /threefoldfoundation/conversion_service/(.*)$ /threefoldfoundation/conversion_service/actors/conversion_service/$1;
        #     }}"""

        #     locations.configure()
        #     website.configure()
        create_gevent_pools()

    def start(self, **kwargs):
        self.install(**kwargs)

    def uninstall(self):
        """Called when package is deleted
        """
        j.sals.nginx.main.websites.default_443.locations.delete("activation_root_proxy")
        j.sals.nginx.main.websites.default_80.locations.delete("activation_root_proxy")

    # def _activate_account(self, address):
    #     self.conversion_wallet.activate_account(address, starting_balance="3.6")

    # def activate_account(self, address):
    #     self.activation_pool.apply(self._activate_account, args=(address,))

    # def _transfer(self, destination_address, amount, asset: str, locked_until=None, memo_hash=None):
    #     issuer_address = asset.split(":")[1]
    #     return self.conversion_wallet.transfer(
    #         destination_address,
    #         amount,
    #         asset,
    #         locked_until,
    #         memo_hash=memo_hash,
    #         fund_transaction=False,
    #         from_address=issuer_address,
    #     )

    # def transfer(self, destination_address, amount, asset: str, locked_until=None, memo_hash=None):
    #     if locked_until:
    #         return self._transfer_locked_tokens(destination_address, amount, asset, locked_until, memo_hash)
    #     else:
    #         asset_code = asset.split(":")[0]
    #         pool = self._tft_issuing_pool if asset_code == "TFT" else self._tfta_issuing_pool
    #         return pool.apply(self._transfer, args=(destination_address, amount, asset, locked_until, memo_hash))

    # def _transfer_locked_tokens(self, destination_address, amount, asset: str, locked_until=None, memo_hash=None):
    #     asset_code = asset.split(":")[0]
    #     asset_issuer = asset.split(":")[1]
    #     import stellar_sdk

    #     escrow_kp = stellar_sdk.Keypair.random()

    #     # delegate to the activation pool
    #     self.activate_account(escrow_kp.public_key)

    #     # no problem using the conversion wallet, just use it's code
    #     self.conversion_wallet.add_trustline(asset_code, asset_issuer, escrow_kp.secret)
    #     preauth_tx = self.conversion_wallet._create_unlock_transaction(escrow_kp, locked_until)
    #     preauth_tx_hash = preauth_tx.hash()
    #     unlock_hash = stellar_sdk.strkey.StrKey.encode_pre_auth_tx(preauth_tx_hash)
    #     self.conversion_wallet._create_unlockhash_transaction(
    #         unlock_hash=unlock_hash, transaction_xdr=preauth_tx.to_xdr()
    #     )
    #     self.conversion_wallet._set_escrow_account_signers(
    #         escrow_kp.public_key, destination_address, preauth_tx_hash, escrow_kp
    #     )

    #     # delegate to the issuing pool
    #     self.transfer(escrow_kp.public_key, amount, asset, memo_hash=memo_hash)

    #     return preauth_tx.to_xdr()
