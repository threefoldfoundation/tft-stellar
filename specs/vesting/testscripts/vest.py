#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import stellar_sdk
from stellar_sdk.transaction_builder import TransactionBuilder, Keypair
import click
from addTrustline import add_trustline
from transfer import transfer


@click.command()
@click.argument("accountsecret", type=str)
@click.argument("fullassetcode", type=str)
@click.option("--amount", type=str, default="1")
def vest_command(accountsecret,fullassetcode, amount):

    split_asset = fullassetcode.split(":", 1)
    asset_code = split_asset[0]
    asset_issuer = split_asset[1]
    # Create keypair from the secret
    kp = stellar_sdk.Keypair.from_secret(accountsecret)
    

    horizon_server = stellar_sdk.Server()
    account=horizon_server.load_account(kp.public_key)
    #Create the escrow account
    escrow_keypair = Keypair.random()
    escrow_address = escrow_keypair.public_key
    txbuilder=TransactionBuilder(account)
    txbuilder.append_create_account_op(escrow_address,"4")
    txe=txbuilder.build()
    txe.sign(kp)
    horizon_server.submit_transaction(txe)
    # Create the trustline
    add_trustline(escrow_keypair.secret,fullassetcode)
    # Set the signing options
    escrow_account=horizon_server.load_account(escrow_address)
    txbuilder=TransactionBuilder(escrow_account)
    txbuilder.append_ed25519_public_key_signer(kp.public_key,1)
    txbuilder.append_set_options_op(master_weight=1,low_threshold=2,med_threshold=2,high_threshold=2)
    txe=txbuilder.build()
    txe.sign(escrow_keypair)
    horizon_server.submit_transaction(txe)
    #Transfer the funds
    transfer(accountsecret,fullassetcode,escrow_address,amount)
    
    print(f"Created escrow account {escrow_address } with {amount} {fullassetcode}")


if __name__ == "__main__":
    vest_command()
