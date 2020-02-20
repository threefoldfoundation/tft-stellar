from Jumpscale import j


class Package(j.baseclasses.threebot_package):
    def start(self):
        for port in (443, 80):
            website = self.openresty.websites.get(f"my_website_{port}")
            website.port = port
            website.ssl = port == 443
            locations = website.locations.get(name=f"my_website_{port}_locations")

            include_location = locations.locations_custom.new()
            include_location.name = f"my_website_includes_{port}"
            # default website locations include wiki related locations
            # so include them
            default_website_name = self.openresty.get_from_port(port).name
            include_location.config = f"""
            include {website.path_cfg_dir}/{default_website_name}_locations/*.conf;

            location /threefoldfoundation/unlock_service {{
                rewrite ^(.+) /threefoldfoundation/unlock_service/actors/unlock_service;
            }}"""

            locations.configure()
            website.configure()