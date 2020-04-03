from Jumpscale import j


class Package(j.baseclasses.threebot_package):
    def start(self):
        DOMAIN = self._package.install_kwargs.get("domain") or "testnet.threefoldtoken.io"
        for port in (443, 80):
            website = self.openresty.get_from_port(port)
            website.ssl = port == 443
            website.domain = DOMAIN

            locations = website.locations.get(name=f"stellar_faucet_{port}_locations")

            include_location = locations.get_location_custom(f"stellar_faucet_includes_{port}")
            include_location.config = f"""
            location /threefoldfoundation/stellar_faucet {{
                rewrite /threefoldfoundation/stellar_faucet/(.*)$ /threefoldfoundation/stellar_faucet/actors/stellar_faucet/$1;
            }}"""

            locations.configure()
            website.configure()
