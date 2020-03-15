from Jumpscale import j


class activation_service(j.baseclasses.threebot_actor):
    def _init(self, **kwargs):
        self.activation_model = j.threebot.packages.threefoldfoundation.activation_service.bcdb.model_get(
            url="threefoldfoundation.activation_service.code_address"
        )

    @j.baseclasses.actor_method
    def create_activation_code(self, address , schema_out, user_session):
        """
      ```in
      address = (S)
      ```
        """
        code_address = self.activation_model.new()
        #TODO: generate random code and check it does not exist yet
        activation_code="qwertyu"
        code_address.code = activation_code
        code_address.address= address

        code_address.save()

        return activation_code #TODO: not just return thi but also the possible phonenumbers
    
    @j.baseclasses.actor_method
    def activate_account(self, activation_code, schema_out, user_session):
        """
      ```in
      activation_code = (S)
      ```
      """
        addresses= self.unlockhash_transaction_model.find(unlockhash=activation_code)
        if not addresses:
            raise j.exceptions.NotFound()
        address_to_activate= addresses[0]
        