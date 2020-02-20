from Jumpscale import j


DOMAIN = "testnet.threefoldtoken.io"

class Package(j.baseclasses.threebot_package):
    def start(self):
        for port in (443, 80):
            website = self.openresty.get_from_port(port)
            website.ssl = port == 443
            website.domain = DOMAIN

            locations = website.locations.get(name=f"unlock_service_{port}_locations")

            include_location = locations.get_location_custom(f"unlock_service_includes_{port}")
            include_location.config = f"""
            location /threefoldfoundation/unlock_service {{
                rewrite /threefoldfoundation/unlock_service/(.*)$ /threefoldfoundation/unlock_service/actors/unlock_service/$1;
            }}"""

            locations.configure()
            website.configure()