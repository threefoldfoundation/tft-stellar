from Jumpscale import j


class Package(j.baseclasses.threebot_package):
    def start(self):
        server = self.openresty
        server.install(reset=False)
        port = 8901

        website = self.openresty.websites.get(f"threefoldfoundation_{port}")
        locations = website.locations.get(name=f"threefoldfoundation_{port}_locations")
        include_location = locations.get_location_custom(f"threefoldfoundation_includes_{port}")

        include_location.config = """
        location /threefoldfoundation/unlock_service {
            rewrite ^(.+) /threefoldfoundation/unlock_service/actors/unlock_service;
        }"""

        locations.configure()
        server.configure()