#!/usr/bin/env python
# pylint: disable=no-value-for-parameter
import click
import os
import sys
import requests
from jumpscale.loader import j


UNLOCK_SERVICE_DEFAULT_HOST = "https://testnet.threefold.io"


@click.command()
@click.option("--source", default="export_data", help="Sourcefile to import data from")
@click.option("--unlock_service_host", default=UNLOCK_SERVICE_DEFAULT_HOST, help="Destination to import data from")
def import_unlockhash_transaction_data(source, unlock_service_host):
    file_content = j.sals.fs.read_file(source)
    for line in file_content.splitlines():
        if "".strip()=="":
            continue
        unlockhash_transaction_data=j.data.serializers.json.loads(line) 
        unlockhash = unlockhash_transaction_data.get("unlockhash")
        transaction_xdr = unlockhash_transaction_data.get("transaction_xdr")

        requests.post(
            f"{unlock_service_host}/threefoldfoundation/unlock_service/create_unlockhash_transaction",
            json={"unlockhash": unlockhash, "transaction_xdr": transaction_xdr},
        )


if __name__ == "__main__":
    import_unlockhash_transaction_data()
