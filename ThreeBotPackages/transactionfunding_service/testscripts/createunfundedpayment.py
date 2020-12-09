#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import stellar_sdk
from stellar_sdk.transaction_builder import Transaction, TransactionEnvelope, Asset, Payment, Keypair
import click


@click.command()
@click.option("--destination", type=str, default="GDAZYYDCTXD6TLMEU3RPG7KOMGKI7RZU676LQMCXO5VOFB4LXVARGMDP")
@click.option("--amount", type=str, default="1")
@click.option("--asset", default="TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3")
@click.option("--from_address", type=str, default="")
def createpayment_transaction(destination, asset, amount, from_address):
    if from_address == "":
        keypair = Keypair.random()
        from_address = keypair.public_key
        print("Generated sending keypair with secret {}".format(keypair.secret))

    split_asset = asset.split(":", 1)
    asset_code = split_asset[0]
    asset_issuer = split_asset[1]

    asset = Asset(code=asset_code, issuer=asset_issuer)
    # Create the transaction

    op = Payment(destination, asset, amount, from_address)
    transaction = Transaction(
        source=stellar_sdk.Keypair.from_public_key(from_address), sequence=1, fee=0, operations=[op]
    )
    transaction_envelope = TransactionEnvelope(
        transaction=transaction, network_passphrase=stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
    )
    print(transaction_envelope.to_xdr())


if __name__ == "__main__":
    createpayment_transaction()
