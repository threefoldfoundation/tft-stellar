from Jumpscale import j

# Should run code  manually in kosmos shell to be able to access bcdb data
# data_json format
# '[{"unlockhash": "abcde", "transaction_xdr": "123456", "id": 1}]'
gedis_service_client = j.clients.gedis.get("gedis_service", package_name="threefoldfoundation.unlock_service")
model = (
    j.data.bcdb.threefoldfoundation__unlock_service.models.threefoldfoundation__unlock_service__unlockhash_transaction
)
data_json = j.data.serializers.json.dumps([obj._ddict for obj in model.find()])
destination = "/unlockhash_transaction_data"
if not j.sal.fs.exists(destination):
    j.sal.fs.touch(destination)
j.sal.fs.writeFile(filename=destination, contents=data_json)
print(f"Data exported successfully to {destination}")

