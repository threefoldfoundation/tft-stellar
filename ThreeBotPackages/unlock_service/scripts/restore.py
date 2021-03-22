#!/usr/bin/env python
# pylint: disable=no-value-for-parameter
import click
import os
import sys
import requests
import json


UNLOCK_SERVICE_DEFAULT_HOSTS = {"test": "https://testnet.threefold.io", "public": "https://tokenservices.threefold.io"}


@click.command()
@click.option("--source", default="export_data", help="Sourcefile to import data from")
@click.option("--network", type=click.Choice(["test", "public"], case_sensitive=False), default="public")
@click.option("--unlock_service_host", default=None, help="Destination to restore to (overrides the network parameter)")
def import_unlockhash_transaction_data(source, network, unlock_service_host):

    if not unlock_service_host:
        unlock_service_host = UNLOCK_SERVICE_DEFAULT_HOSTS[network]
    print(f"Restoring data to {unlock_service_host} from {source}\n")

    with open(source,mode="r") as f:
        
        for line in f.readlines():
            if line.strip() == "":
                continue
            unlockhash_transaction_data = json.loads(line)
            unlockhash = unlockhash_transaction_data.get("unlockhash")
            transaction_xdr = unlockhash_transaction_data.get("transaction_xdr")

            r = requests.post(
                f"{unlock_service_host}/threefoldfoundation/unlock_service/create_unlockhash_transaction",
                json={"unlockhash": unlockhash, "transaction_xdr": transaction_xdr},
            )
            r.raise_for_status()


if __name__ == "__main__":
    import_unlockhash_transaction_data()
