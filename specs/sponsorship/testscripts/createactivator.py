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
def create_account():
    keypair = Keypair.random()
    address = keypair.public_key
    print(f"Generated account {address } with secret {keypair.secret}")
    activate_through_friendbot(address)
    print(f"Account activated through friendbot")


if __name__ == "__main__":
    create_account()
