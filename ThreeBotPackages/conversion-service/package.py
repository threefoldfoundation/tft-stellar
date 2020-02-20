from Jumpscale import j


class Package(j.baseclasses.threebot_package):
    def start(self):
        for port in (443, 80):
            website = self.openresty.get_from_port(port)
            locations = website.locations.get(name=f"conversion_service_{port}_locations")

            include_location = locations.get_location_custom(f"conversion_service_includes_{port}")
            include_location.config = f"""
            location /threefoldfoundation/conversion_service {{
                rewrite /threefoldfoundation/conversion_service/(.*)$ /threefoldfoundation/conversion_service/actors/conversion_service/$1;
            }}"""

            locations.configure()
            website.configure()