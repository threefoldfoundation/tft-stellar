from Jumpscale import j


class Package(j.baseclasses.threebot_package):
    def start(self):
        for port in (443, 80):
            website = self.openresty.websites.get(f"unlock_service_{port}")
            website.port = port
            website.ssl = port == 443
            locations = website.locations.get(name=f"unlock_service_{port}_locations")

            include_location = locations.locations_custom.new()
            include_location.name = f"unlock_service_includes_{port}"
            # default website locations include wiki related locations
            # so include them
            default_website_name = self.openresty.get_from_port(port).name
            include_location.config = f"""
            include {website.path_cfg_dir}/{default_website_name}_locations/*.conf;

            location / {{
                rewrite ^(.+) /threefoldfoundation/unlock_service/actors/unlock_service;
            }}"""

            locations.configure()
            website.configure()