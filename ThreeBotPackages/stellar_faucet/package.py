from Jumpscale import j


class Package(j.baseclasses.threebot_package):
    def start(self):
        DOMAIN = self._package.install_kwargs.get("domain","testnet.threefoldtoken.io") 
        for port in (443, 80):
            website = self.openresty.get_from_port(port)
            website.ssl = port == 443
            website.domain = DOMAIN

            locations = website.locations.get(name=f"faucet_locations_{port}")

            # faucet_proxy_location = locations.get_location_proxy(f"faucet_location_{port}")
            # faucet_proxy_location.path_url = "/faucet"
            # faucet_proxy_location.ipaddr_dest = "127.0.0.1"
            # faucet_proxy_location.port_dest = 8080
            include_location = locations.get_location_custom(f"faucet_includes_{port}")
            include_location.config = f"""
            location /threefoldfoundation/stellar_faucet {{
                try_files $uri $uri/ /index.html;
            }}"""
            include_location.is_auth = False 

            locations.configure()
            website.configure()

            # self._start_faucet_app()

    def _start_faucet_app(self, reset=True):
        s = j.servers.startupcmd.get("faucet")
        s.cmd_start = f"""
        cd {self.package_root}
        cd faucet_frontend
        npm run serve
        """
        s.executor = "tmux"
        s.interpreter = "bash"
        s.timeout = 1000
        s.ports = [8080]

        s.start(reset=reset)
