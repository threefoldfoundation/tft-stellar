from Jumpscale import j


class Package(j.baseclasses.threebot_package):
    def start(self):
        server = self.openresty
        server.install(reset=False)
        port = 8901

        website = server.get_from_port(port)
        locations = website.locations.get()
        actor_location = locations.locations_custom.new()
        actor_location.name = "unlock_service"

        actor_location.config = """
        location /threefoldfoundation/unlock_service {
            rewrite ^(.+) /threefoldfoundation/unlock_service/actors/unlock_service;
        }"""

        locations.configure()
        server.configure()