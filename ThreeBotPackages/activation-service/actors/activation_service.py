from Jumpscale import j



class activation_service(j.baseclasses.threebot_actor):

    def _stellar_address_used_before(self, stellar_address):
        try:
            stellar_client = j.clients.stellar.get("activation_wallet")
            from stellar_sdk.exceptions import NotFoundError

            stellar_client.list_transactions(address=stellar_address)
        except NotFoundError:
            return False
        else:
            return True

    def _activate_account(self, address):
        if self._stellar_address_used_before(address):
            raise j.exceptions.Base("This address is not new")
        activationwallet = j.clients.stellar.get("activation_wallet")
        activationwallet.activate_account(address, starting_balance="3.6")
    
    @j.baseclasses.actor_method
    def create_activation_code(self, address, schema_out, user_session):
        """
        ```in
        address = (S)
        ```
        ```out
        activation_code = (S)
        address = (S)
        phonenumbers= (LS)
        """
        self._activate_account(address)
        response = j.data.serializers.json.dumps(
            {"activation_code": "abcd", "address": address, "phonenumbers": ["+1234567890"]}
        )
        return response

    @j.baseclasses.actor_method
    def activate_account(self, activation_code, schema_out, user_session):
        """
        ```in
        activation_code = (S)
        ```
        """
        return None
