from Jumpscale import j
import gevent


class Package(j.baseclasses.threebot_package):
    def start(self):

        conversion_wallet_name = self._package.install_kwargs.get("wallet","converter")
        
        self.conversion_wallet= j.clients.stellar.get(conversion_wallet_name)

        DOMAIN = self._package.install_kwargs.get("domain","testnet.threefoldtoken.io")
        for port in (443, 80):
            website = self.openresty.get_from_port(port)
            website.ssl = port == 443
            website.domain = DOMAIN

            locations = website.locations.get(name=f"conversion_service_{port}_locations")

            include_location = locations.get_location_custom(f"conversion_service_includes_{port}")
            include_location.is_auth = False
            include_location.config = f"""
            location /threefoldfoundation/conversion_service {{
                rewrite /threefoldfoundation/conversion_service/(.*)$ /threefoldfoundation/conversion_service/actors/conversion_service/$1;
            }}"""

            locations.configure()
            website.configure()
        self.pool= gevent.pool.Pool(1)

    def _activate_account(self, address):
        self.conversion_wallet.activate_account(address, starting_balance="3.6")
                
    def activate_account(self, address):
        self.pool.apply(self._activate_account, args=(address,))

    def _transfer(
        self,
        destination_address,
        amount,
        asset="XLM",
        locked_until=None,
        memo_hash=None,
    ):
        return self.conversion_wallet.transfer(destination_address,amount,asset,locked_until, memo_hash=memo_hash) 

    def transfer(
        self,
        destination_address,
        amount,
        asset="XLM",
        locked_until=None,
        memo_hash=None,
    ):
        return self.pool.apply(self._transfer, args=(destination_address,amount,asset,locked_until,memo_hash))

    def stop(self):
        if self.pool:
            self.pool.kill()
            self.pool = None