#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import stellar_sdk
from stellar_sdk.transaction_builder import Keypair
import click
import requests


def activate_through_friendbot(address: str):
    """
    Activates and funds a testnet account using friendbot
    """
    resp = requests.get(url="https://friendbot.stellar.org", params={"addr": address})
    resp.raise_for_status()


@click.command()
@click.option("--tokencode", type=str, default="VEST")
def create_token(tokencode):
    keypair = Keypair.random()
    issuer_address = keypair.public_key
    print(f"Generated issuer account {issuer_address } with secret {keypair.secret}")
    activate_through_friendbot(issuer_address)
    print(f"Issuer account activated through friendbot")
    print(f"Asset: {tokencode}:{issuer_address}")


if __name__ == "__main__":
    create_token()
