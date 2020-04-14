#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import stellar_sdk
from stellar_sdk.transaction_builder import TransactionBuilder
import click


@click.command()
@click.argument("destination", type=str)
@click.option("--amount", type=str, default="1")
@click.option("--asset", default="TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3")
@click.option("--from_secret", type=str, required=True)
@click.option("--funder_secret", type=str, required=True)
def send_asset_to_account(destination, asset, amount, from_secret, funder_secret):
    split_asset = asset.split(":", 1)
    asset_code = split_asset[0]
    asset_issuer = split_asset[1]
    # Create keypairs from the secrets
    from_kp = stellar_sdk.Keypair.from_secret(from_secret)
    funder_kp = stellar_sdk.Keypair.from_secret(funder_secret)

    # load the funder account
    horizon_server = stellar_sdk.Server()
    funder_account = horizon_server.load_account(funder_kp.public_key)

    # Create the transaction
    transaction = (
        TransactionBuilder(funder_account)
        .append_payment_op(destination, amount, asset_code, asset_issuer, source=from_kp.public_key)
        .build()
    )
    transaction.sign(from_kp)
    transaction.sign(funder_kp)
    response = horizon_server.submit_transaction(transaction)
    print(response)
    print(
        "Sent {amount} {asset} from {from_address} to {destination} funded by {funder_address}".format(
            amount=amount,
            asset=asset,
            from_address=from_kp.public_key,
            destination=destination,
            funder_address=funder_kp.public_key,
        )
    )


if __name__ == "__main__":
    send_asset_to_account()
