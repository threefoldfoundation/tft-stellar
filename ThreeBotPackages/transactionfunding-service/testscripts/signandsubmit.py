#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import stellar_sdk
from stellar_sdk.transaction_builder import TransactionBuilder
import click

@click.command()
@click.argument('transaction', type=str)
@click.option('--secret', type=str, required=True)
def sign_and_submit(transaction,secret):
    #Create keypairs from the secrets
    kp= stellar_sdk.Keypair.from_secret(secret)

    horizon_server=stellar_sdk.Server()

    txe=stellar_sdk.TransactionEnvelope.from_xdr(transaction,stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE)
    transaction.sign(kp)
    response=horizon_server.submit_transaction(txe)
    print(response)
   

if __name__ == '__main__':
  sign_and_submit()