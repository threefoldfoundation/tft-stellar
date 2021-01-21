# pylint: disable=no-value-for-parameter
import click
import os
import sys
import requests
from jumpscale.loader import j
from jumpscale.core.base import StoredFactory


UNLOCK_SERVICE_DEFAULT_HOST = "https://testnet.threefoldtoken.io"


@click.command()
@click.option("--source", default="/unlockhash_transaction_data", help="Sourcefile to import data from")
@click.option("--unlock_service_host", default=UNLOCK_SERVICE_DEFAULT_HOST, help="Destination to import data from")
def import_unlockhash_transaction_data(source, unlock_service_host):
    file_content = j.sals.fs.read_file(source)
    file_content = file_content.replace("'", "")
    unlockhash_transactions_list = j.data.serializers.json.loads(file_content)
    for unlockhash_transaction_data in unlockhash_transactions_list:
        unlockhash = unlockhash_transaction_data.get("unlockhash")
        transaction_xdr = unlockhash_transaction_data.get("transaction_xdr")

        requests.post(
            f"{unlock_service_host}/threefoldfoundation/unlock_service/create_unlockhash_transaction",
            json={"unlockhash": unlockhash, "transaction_xdr": transaction_xdr},
        )

if __name__ == "__main__":
    import_unlockhash_transaction_data()
