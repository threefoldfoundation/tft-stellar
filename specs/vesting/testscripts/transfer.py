#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import stellar_sdk
from stellar_sdk.transaction_builder import TransactionBuilder, Keypair
import click


def transfer(accountsecret, fullassetcode, destination, amount):

    split_asset = fullassetcode.split(":", 1)
    asset_code = split_asset[0]
    asset_issuer = split_asset[1]
    # Create keypair from the secret
    kp = stellar_sdk.Keypair.from_secret(accountsecret)

    horizon_server = stellar_sdk.Server()
    account = horizon_server.load_account(kp.public_key)
    txbuilder = TransactionBuilder(account)
    txbuilder.append_payment_op(destination, amount, asset_code, asset_issuer)
    txe = txbuilder.build()
    txe.sign(kp)
    horizon_server.submit_transaction(txe)


@click.command()
@click.argument("accountsecret", type=str)
@click.argument(
    "destination",
    type=str,
)
@click.option("--amount", type=str, default="1")
@click.option("--fullassetcode", type=str, default="TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3")
def transfer_command(accountsecret, fullassetcode, destination, amount):
    transfer(accountsecret, fullassetcode, destination, amount)


if __name__ == "__main__":
    transfer_command()
