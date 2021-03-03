#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import stellar_sdk
from stellar_sdk.transaction_builder import TransactionBuilder
import click


def add_trustline(accountsecret:str, fullassetcode:str):
    splitassetcode=fullassetcode.split(":")
    # Create keypair from the secret
    kp = stellar_sdk.Keypair.from_secret(accountsecret)

    horizon_server = stellar_sdk.Server()
    account=horizon_server.load_account(kp.public_key)
    txbuilder=TransactionBuilder(account)
    txbuilder.append_change_trust_op(splitassetcode[0],splitassetcode[1])
    txe=txbuilder.build()
    txe.sign(kp)
    horizon_server.submit_transaction(txe)

@click.command()
@click.argument("accountsecret", type=str)
@click.argument("fullassetcode", type=str)
def add_trustline_command(accountsecret, fullassetcode):
    add_trustline(accountsecret,fullassetcode)


if __name__ == "__main__":
    add_trustline_command()
