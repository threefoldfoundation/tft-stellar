#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import stellar_sdk
from stellar_sdk.transaction_builder import Keypair
import click
import json
import requests



def activate_through_friendbot(address: str):
    """
    Activates and funds a testnet account using friendbot
    """
    resp = requests.get(url="https://friendbot.stellar.org", params={"addr": address})
    resp.raise_for_status()


@click.command()
@click.argument("outputfile", default="cosigners.json",type=click.File(mode="w"))
def create_cosigners(outputfile):
    cosigners=[]
    for i in range(9):
        keypair = Keypair.random()
        address = keypair.public_key
        print(f"Generated account {address } with secret {keypair.secret}")
        activate_through_friendbot(address)
        print(f"Account activated through friendbot")
        cosigners.append({"address":address,"secret":keypair.secret})
    json.dump(cosigners,outputfile)


if __name__ == "__main__":
    create_cosigners()
