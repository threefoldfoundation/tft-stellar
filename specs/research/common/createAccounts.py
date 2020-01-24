#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import stellar_sdk
import click
import requests
import decimal

def create_keypair():
    kp = stellar_sdk.Keypair.random()
    print("Key: {}".format(kp.secret))
    print("Address: {}".format(kp.public_key))
    return kp

def activate_account_through_friendbot(address):
    response = requests.get('https://friendbot.stellar.org/?addr={}'.format(address))
    response.raise_for_status()
    print("account \'{}\' activated through friendbot".format(address))

def activate_account(address, source_keypair, starting_balance=2):
    horizon_server=stellar_sdk.Server()
    source_account=horizon_server.load_account(source_keypair.public_key)
    tx= stellar_sdk.transaction_builder.TransactionBuilder(source_account).append_create_account_op(
        address,
        starting_balance=decimal.Decimal(value=starting_balance)
    ).build()
    tx.sign(source_keypair)
    response=horizon_server.submit_transaction(tx)
    print(response)
    print("account \'{}\' activated with {balance} XLM".format(address, balance=starting_balance)) 


@click.command()
@click.argument('name', type=str,nargs=-1)
def create_accounts(name):
    for accountname in name:
        print('Creating \'{name}\' keypair'.format(name=accountname))
        kp = create_keypair()
        activate_account_through_friendbot(kp.public_key)

if __name__ == '__main__':
  create_accounts()
