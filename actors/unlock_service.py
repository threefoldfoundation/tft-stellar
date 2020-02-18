from Jumpscale import j


class Unlock_service(j.baseclasses.threebot_actor):
    def _init(self, **kwargs):
        self.unlockhash_transaction_model = j.threebot.packages.threefoldfoundation.tft_stellar.bcdb.model_get(
            url="threefoldfoundation.tft_stellar.unlockhash_transaction"
        )

    @j.baseclasses.actor_method
    def create_unlockhash_transaction(self, unlockhash_transaction, schema_out, user_session):
        """
      ```in
      unlockhash_transaction = (O) !threefoldfoundation.tft_stellar.unlockhash_transaction
      ```

      ```out
      unlockhash_transaction = (O) !threefoldfoundation.tft_stellar.unlockhash_transaction
      ```
      """
        unlockhash_transaction = self.unlockhash_transaction_model.new(unlockhash_transaction).save()
        return unlockhash_transaction

    @j.baseclasses.actor_method
    def get_unlockhash_transaction(self, unlockhash, schema_out, user_session):
        """
      ```in
      unlockhash = (S)
      ```

      ```out
      !threefoldfoundation.tft_stellar.unlockhash_transaction
      ```
      """
        try:
            transactions = self.unlockhash_transaction_model.find(unlockhash=unlockhash)
            if not transactions:
                raise j.exceptions.NotFound()
            return transactions[0]
        except j.exceptions.NotFound:
            raise j.exceptions.NotFound("unlocktransaction with hash %s not found" % unlockhash)
