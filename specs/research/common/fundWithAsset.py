#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
import stellar_sdk
from stellar_sdk.transaction_builder import TransactionBuilder

def send_asset_to_account(destination,asset,amount,source, signer):
    split_asset= asset.split(':',1)
    asset_code=split_asset[0]
    asset_issuer=split_asset[1]
    horizon_server=stellar_sdk.Server()
    source_account=horizon_server.load_account(source)
    transaction = TransactionBuilder(source_account).append_payment_op(
        destination,
        amount,
        asset_code,
        asset_issuer).build()
    for sk in signer:
        kp=stellar_sdk.Keypair.from_secret(sk)
        transaction.sign(kp)
    response=horizon_server.submit_transaction(transaction)
    print(response)
    print('Sent {amount} {asset} to {destination}'.format(
        amount=amount,
        asset=asset,
        destination=destination
    ))

@click.command()
@click.argument('destination', type=str)
@click.option('--amount', type=str,default='10')
@click.option('--asset',default='TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3')
@click.option('--source', type=str, default='GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3')
@click.option('--signer', multiple=True, required=True,help='Secret key of a required signer')
def send_asset_to_account_command(destination,asset,amount,source, signer):
    send_asset_to_account(destination,asset,amount,source, signer)

if __name__ == '__main__':
  send_asset_to_account()