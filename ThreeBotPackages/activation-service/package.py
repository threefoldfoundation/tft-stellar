from Jumpscale import j


class Package(j.baseclasses.threebot_package):
    def start(self):

        activation_wallet_name= = self._package.install_kwargs.get("wallet","activation_wallet")
        
        self.activation_wallet= j.clients.stellar.get(activation_wallet_name)

        DOMAIN = self._package.install_kwargs.get("domain") or "testnet.threefoldtoken.io"
        for port in (443, 80):
            website = self.openresty.get_from_port(port)
            website.ssl = port == 443
            website.domain = DOMAIN

            locations = website.locations.get(name=f"activation_service_{port}_locations")

            include_location = locations.get_location_custom(f"activation_service_includes_{port}")
            include_location.is_auth = False
            include_location.config = """
            location /threefoldfoundation/activation_service {
                rewrite /threefoldfoundation/activation_service/(.*)$ /threefoldfoundation/activation_service/actors/activation_service/$1;
            }"""

            locations.configure()
            website.configure()
         self._start_activation_loop()

    def _start_activation_loop():
        print("Starting activation service loop")
        # create gevent queueu
        self.queue = gevent.queue.Queue()
        # start gevent loop at _funding_loop
        self._activation_greenlet = gevent.spawn(self._activation_loop)

    def _activation_loop(self)
        for address in self.queue:
            try:
                self.activation_wallet.activate_account(address, starting_balance="3.6")
                 #TODO signal caller
            except Exception e:
                #TODO: return exception to caller
    
    def activate_account(self, address):
         # add address to gevent queue
        self.queue.put(address)
        #TODO wait for processing to finish


    def _stop_activation_loop(self):
        print("Halting activation service loop")
        self._activation_greenlet.kill()

    def stop(self):
        self._stop_activation_loop()