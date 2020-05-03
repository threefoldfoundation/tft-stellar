from Jumpscale import j
import gevent


class Package(j.baseclasses.threebot_package):
    def start(self):

        activation_wallet_name = self._package.install_kwargs.get("wallet","activation_wallet")
        
        self.activation_wallet= j.clients.stellar.get(activation_wallet_name)

        DOMAIN = self._package.install_kwargs.get("domain") or "testnet.threefoldtoken.io"
        for port in (443, 80):
            website = self.openresty.get_from_port(port)
            website.ssl = port == 443
            website.domain = DOMAIN

            locations = website.locations.get(name=f"activation_service_{port}_locations")

            include_location = locations.get_location_custom(f"activation_service_includes_{port}")
            include_location.is_auth = False
            include_location.config = """
            location /threefoldfoundation/activation_service {
                rewrite /threefoldfoundation/activation_service/(.*)$ /threefoldfoundation/activation_service/actors/activation_service/$1;
            }"""

            locations.configure()
            website.configure()
        self.pool= gevent.pool.Pool(1)

    def _activate_account(self, address):
        self.activation_wallet.activate_account(address, starting_balance="3.6")
                
    def activate_account(self, address):
        self.pool.apply(self._activate_account, args=(address,))

    def stop(self):
        if self.pool:
            self.pool.kill()
            self.pool = None