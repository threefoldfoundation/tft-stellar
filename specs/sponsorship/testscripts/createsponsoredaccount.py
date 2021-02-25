#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import stellar_sdk
from stellar_sdk.transaction_builder import Keypair
import click

def activate_account(source_keypair, new_account_kp, fullassetcode):
    split_asset = fullassetcode.split(":", 1)
    asset_code = split_asset[0]
    asset_issuer = split_asset[1]
    new_account_address=new_account_kp.public_key

    horizon_server = stellar_sdk.Server()

    source_account = horizon_server.load_account(source_keypair.public_key)

    base_fee = horizon_server.fetch_base_fee()
    transaction = (
        stellar_sdk.TransactionBuilder(
            source_account=source_account,
            network_passphrase=stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
        .append_begin_sponsoring_future_reserves_op(new_account_address)
        .append_create_account_op(destination=new_account_address, starting_balance="0")
        .append_change_trust_op(asset_issuer=asset_issuer, asset_code=asset_code, source=new_account_address)
        .append_end_sponsoring_future_reserves_op(new_account_address)
        .set_timeout(60)
        .build()
    )
    transaction.sign(source_keypair)
    transaction.sign(new_account_kp)
    horizon_server.submit_transaction(transaction)

@click.command()
@click.argument("activatorsecret", type=str)
@click.argument("fullassetcode", type=str)
def create_account(activatorsecret,fullassetcode):
    activator_kp=Keypair.from_secret(activatorsecret)
    keypair = Keypair.random()
    address = keypair.public_key
    activate_account(activator_kp,keypair,fullassetcode)
    print(f"Activated account {address } with secret {keypair.secret}")


if __name__ == "__main__":
    create_account()