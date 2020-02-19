from Jumpscale import j


class unlock_service(j.baseclasses.threebot_actor):
    def _init(self, **kwargs):
        self.unlockhash_transaction_model = j.threebot.packages.threefoldfoundation.tft_stellar.unlock_service.bcdb.model_get(
            url="threefoldfoundation.tft_stellar.unlock_service.unlockhash_transaction"
        )

    @j.baseclasses.actor_method
    def create_unlockhash_transaction(self, unlockhash, transaction_xdr, schema_out, user_session):
        """
      ```in
      unlockhash = (S)
      transaction_xdr = (S)
      ```

      ```out
      unlockhash_transaction = (O) !threefoldfoundation.tft_stellar.unlock_service.unlockhash_transaction
      ```
      """
        unlockhash_transaction = self.unlockhash_transaction_model.new()

        unlockhash_transaction.unlockhash = unlockhash
        unlockhash_transaction.transaction_xdr = transaction_xdr

        unlockhash_transaction.save()

        return unlockhash_transaction

    @j.baseclasses.actor_method
    def get_unlockhash_transaction(self, unlockhash, schema_out, user_session):
        """
      ```in
      unlockhash = (S)
      ```

      ```out
      !threefoldfoundation.tft_stellar.unlock_service.unlockhash_transaction
      ```
      """
        try:
            transactions = self.unlockhash_transaction_model.find(unlockhash=unlockhash)
            if not transactions:
                raise j.exceptions.NotFound()
            return transactions[0]
        except j.exceptions.NotFound:
            raise j.exceptions.NotFound("unlocktransaction with hash %s not found" % unlockhash)

    @j.baseclasses.actor_method
    def list(self, schema_out=None, user_session=None):
        """
        ```out
        unlockhash_transactions = (LO) !threefoldfoundation.tft_stellar.unlockhash_transaction
        ```
        """
        out = schema_out.new()
        for unlockhash_tx in self.unlockhash_transaction_model.iterate():
            out.unlockhash_transactions.append(unlockhash_tx)
        return out