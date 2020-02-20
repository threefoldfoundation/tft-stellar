from Jumpscale import j


class Package(j.baseclasses.threebot_package):
    def start(self):
        server = self.openresty
        server.install(reset=False)

        for port in (443, 80):
            website = server.get_from_port(port)
            locations = website.locations.get()
            include_location = locations.locations_custom.new()
            include_location.name = f"unlock_service_{port}"

            default_website_name = self.openresty.get_from_port(port).name

            include_location.config = """
            include {website.path_cfg_dir}/{default_website_name}_locations/*.conf;
            location /threefoldfoundation/unlock_service {
                rewrite ^(.+) /threefoldfoundation/unlock_service/actors/unlock_service;
            }"""

            locations.configure()
            website.configure()

        server.configure()
