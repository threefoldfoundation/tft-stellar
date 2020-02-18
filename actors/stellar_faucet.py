from Jumpscale import j


class stellar_faucet(j.baseclasses.threebot_actor):
    @j.baseclasses.actor_method
    def transfer(self, destination, schema_out=None, user_session=None):
        distributor = j.clients.stellar.get("distributor")
        distributor.network = "TEST"

        distributor.secret = self.package.install_kwargs.get("secret")
        issuer = self.package.install_kwargs.get("issuer")
        amount = self.package.install_kwargs.get("amount")

        asset = "tft:" + issuer

        try:
            distributor.transfer(destination_address=destination, amount=amount, asset=asset)
        except Exception as e:
            raise e
