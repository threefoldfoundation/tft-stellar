#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import stellar_sdk
from stellar_sdk.transaction_builder import Transaction, TransactionEnvelope, Asset, Payment, Keypair
import click


@click.command()
@click.argument("accountsecret", type=str)
@click.argument("destination", type=str)
@click.argument("feedestination", type=str)
@click.option("--amount", type=str, default="1")
@click.option("--fee", type=str, default="0.01")
@click.option("--asset", default="TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3")
@click.option("--network", default="test", type=click.Choice(["test", "public"], case_sensitive=False))
def createpayment_transaction(accountsecret, destination, feedestination, fee, asset, amount, network):

    network_passphrase = (
        stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
        if network == "test"
        else stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE
    )
    horizon_server = stellar_sdk.Server(
        "https://horizon-testnet.stellar.org" if network == "test" else "https://horizon.stellar.org"
    )

    keypair = Keypair.from_secret(accountsecret)
    from_address = keypair.public_key

    split_asset = asset.split(":", 1)
    asset_code = split_asset[0]
    asset_issuer = split_asset[1]

    source_account = horizon_server.load_account(from_address)
    txe = (
        stellar_sdk.TransactionBuilder(source_account=source_account, network_passphrase=network_passphrase, base_fee=0)
        .append_payment_op(destination, amount, asset_code=asset_code, asset_issuer=asset_issuer)
        .append_payment_op(feedestination, fee, asset_code=asset_code, asset_issuer=asset_issuer)
        .set_timeout(60*3)
        .build()
    )

    txe.sign(keypair)
    print(txe.to_xdr())


if __name__ == "__main__":
    createpayment_transaction()
