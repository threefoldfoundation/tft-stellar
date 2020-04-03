from Jumpscale import j


class stellar_faucet(j.baseclasses.threebot_actor):
    @j.baseclasses.actor_method
    def transfer(self, destination, username, schema_out=None, user_session=None):
        distributor = j.clients.stellar.get("distributor")

        distributor.network = self.package.install_kwargs.get("network")
        distributor.secret = self.package.install_kwargs.get("secret")

        asset = self.package.install_kwargs.get("asset")
        amount = self.package.install_kwargs.get("amount")

        txes = distributor.list_transaction(address=destination)
        for tx in txes:
            if tx.memo_text == username:
                raise Exception("user already requested token")

        try:
            distributor.transfer(destination_address=destination, amount=amount, asset=asset, memo_text=username)
        except Exception as e:
            raise e
