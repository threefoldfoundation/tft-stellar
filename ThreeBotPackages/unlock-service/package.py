from Jumpscale import j


class Package(j.baseclasses.threebot_package):
    def start(self):
        server = self.openresty
        server.install(reset=False)

        for port in (443, 80):
            website = server.get_from_port(port)
            locations = website.locations.get()
            actor_location = locations.locations_custom.new()
            actor_location.name = f"unlock_service_{port}"

            actor_location.config = """
            location /threefoldfoundation/unlock_service {
                rewrite ^(.+) /threefoldfoundation/unlock_service/actors/unlock_service;
            }"""

            locations.configure()

        server.configure()
