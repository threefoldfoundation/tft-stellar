#!/usr/bin/env python

import stellar_sdk
import click
import requests

def create_Keypair(name=''):
    print('Creating \'{name}\' keypair'.format(name=name))
    kp = stellar_sdk.Keypair.random()
    print("Key: {}".format(kp.secret))
    print("Address: {}".format(kp.public_key))
    return kp

def activate_account(address):
    res = requests.get('https://friendbot.stellar.org/?addr={}'.format(address))
    res.raise_for_status()
    print("account \'{}\' activated through friendbot".format(address))
 
@click.command()
def create_accounts():
    kp = create_Keypair('from')
    activate_account(kp.public_key)
    kp = create_Keypair('to')
    activate_account(kp.public_key)
    kp= create_Keypair('funding')
    activate_account(kp.public_key)

if __name__ == '__main__':
  create_accounts()
