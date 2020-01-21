#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import stellar_sdk
from stellar_sdk.transaction_builder import TransactionBuilder
import click

def add_trustline(secret_key, asset_code, asset_issuer):
    kp= stellar_sdk.Keypair.from_secret(secret_key)
    horizon_server = stellar_sdk.Server()
    account= horizon_server.load_account(kp.public_key)
    transaction=TransactionBuilder(account).append_change_trust_op(asset_code,asset_issuer).build()
    transaction.sign(kp)
    response=horizon_server.submit_transaction(transaction)
    print(response)
    print('Added trustline to {asset_code}:{asset_issuer} for account {address}'.format(asset_code=asset_code,asset_issuer=asset_issuer,address=kp.public_key))

@click.command()
@click.argument('secret_key', nargs=-1)
@click.option('--asset',default='TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3')
def add_trustlines(secret_key, asset):
    split_asset= asset.split(':',1)
    asset_code=split_asset[0]
    asset_issuer=split_asset[1]
    for sk in secret_key:
        add_trustline(sk,asset_code,asset_issuer)

if __name__ == '__main__':
  add_trustlines()