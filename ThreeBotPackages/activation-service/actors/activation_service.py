from Jumpscale import j

import random, string


class activation_service(j.baseclasses.threebot_actor):
    def _init(self, **kwargs):
        self.activation_model = j.threebot.packages.threefoldfoundation.activation_service.bcdb.model_get(
            url="threefoldfoundation.activation_service.code_address"
        )

    def _generate_activation_code(self):
        def create_code(k):
           return ''.join(random.sample(string.ascii_lowercase,k)) 
        for codelength in range(5,7):
            for i in range(3):
                code=create_code(codelength)
                existing=self.activation_model.find(code=code)
                if not existing:
                    return code
        raise j.exceptions.Base("Failed") 

    @j.baseclasses.actor_method
    def create_activation_code(self, address , schema_out, user_session):
        """
        ```in
        address = (S)
        ```
        ```out
        activation_code = (S)
        address = (S)
        phonenumbers= (LS)
        """
        code_address = self.activation_model.new()

        activation_code=self._generate_activation_code()
        code_address.code = activation_code
        code_address.address= address

        code_address.save()
        response=j.data.serializers.json.dumps({"activation_code":code_address,"address":address,"phonenumbers":["+1234567890",]})
        return response 
    
    @j.baseclasses.actor_method
    def activate_account(self, activation_code, schema_out, user_session):
        """
      ```in
      activation_code = (S)
      ```
      """
        addresses= self.activation_model.find(code=activation_code)
        if not addresses:
            raise j.exceptions.NotFound()
        address_to_activate= addresses[0]
        