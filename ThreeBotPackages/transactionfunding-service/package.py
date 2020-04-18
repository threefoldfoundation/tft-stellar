from Jumpscale import j


class Package(j.baseclasses.threebot_package):
    def ensure_slavewallets(self):
        main_walletname = self._package.install_kwargs.get("wallet", "txfundingwallet")
        main_wallet = j.clients.stellar.get(main_walletname)
        nr_of_slaves = self._package.install_kwargs.get("slaves", 30)
        for slaveindex in range(nr_of_slaves):
            walletname = main_walletname + "_" + str(slaveindex)
            if not j.clients.stellar.exists(walletname):
                slave_wallet = j.clients.stellar.new(walletname, network=main_wallet.network)
                main_wallet.activate_account(slave_wallet.address, starting_balance="5")

    def start(self):
        self.ensure_slavewallets()
        DOMAIN = self._package.install_kwargs.get("domain") or "testnet.threefoldtoken.io"
        for port in (443, 80):
            website = self.openresty.get_from_port(port)
            website.ssl = port == 443
            website.domain = DOMAIN

            locations = website.locations.get(name=f"transactionfunding_service_{port}_locations")

            include_location = locations.get_location_custom(f"transactionfunding_service_includes_{port}")
            include_location.is_auth = False
            include_location.config = f"""
            location /threefoldfoundation/transactionfunding_service {{
                rewrite /threefoldfoundation/transactionfunding_service/(.*)$ /threefoldfoundation/transactionfunding_service/actors/transactionfunding_service/$1;
            }}"""

            locations.configure()
            website.configure()
