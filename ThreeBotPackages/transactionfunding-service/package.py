from Jumpscale import j
import gevent
import gevent.queue
from decimal import Decimal


class Package(j.baseclasses.threebot_package):
    def get_main_fundingwallet(self):
        main_walletname = self._package.install_kwargs.get("wallet", "txfundingwallet")
        main_wallet = j.clients.stellar.get(main_walletname)
        return main_wallet

    def ensure_slavewallets(self):
        main_wallet = self.get_main_fundingwallet()
        nr_of_slaves = self._package.install_kwargs.get("slaves", 30)
        for slaveindex in range(nr_of_slaves):
            walletname = str(main_wallet.name) + "_" + str(slaveindex)
            if not j.clients.stellar.exists(walletname):
                print(f"activating slave {walletname}")
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
            include_location.config = """
            location /threefoldfoundation/transactionfunding_service {
                rewrite /threefoldfoundation/transactionfunding_service/(.*)$ /threefoldfoundation/transactionfunding_service/actors/transactionfunding_service/$1;
            }"""

            locations.configure()
            website.configure()
        self._start_funding_loop()

    def _start_funding_loop(self):
        print("Starting transaction funding service refund loop")
        # create gevent queueu
        self.queue = gevent.queue.Queue()
        # start gevent loop at _funding_loop
        self._funding_greenlet = gevent.spawn(self._funding_loop)

    def _funding_loop(self):
        for walletname in self.queue:
            try:
                wallet = j.clients.stellar.get(walletname)
                balances = wallet.get_balance()
                xlmbalance = [b for b in balances.balances if b.is_native][0]
                xlmbalance = Decimal(xlmbalance.balance)
                # if xlmbalance< 3 add 2 from main fundingwallet
                if xlmbalance < Decimal("3"):
                    print(f"Refunding {walletname}")
                    self.get_main_fundingwallet().transfer(wallet.address, "2", asset="XLM", fund_transaction=False)
            except Exception as e:
                print(f"Exception in transaction funding service loop: {e}")

    def fund_if_needed(self, walletname):
        # add walletname to gevent queue
        self.queue.put(walletname)

        return None

    def _stop_funding_loop(self):
        print("Halting transaction funding service refund loop")
        self._funding_greenlet.kill()

    def stop(self):
        self._stop_funding_loop()
