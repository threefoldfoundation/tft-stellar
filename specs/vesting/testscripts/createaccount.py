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


def create_account() -> map:
    keypair = Keypair.random()
    return {"address": keypair.public_key, "secret": keypair.secret}


def create_activated_account() -> map:
    account = create_account()
    address = account["address"]
    activate_through_friendbot(address)
    return account


@click.command()
def create_account_command():
    account = create_activated_account()
    print(f"Generated account {account['address']} with secret {account['secret']}")


if __name__ == "__main__":
    create_account_command()
