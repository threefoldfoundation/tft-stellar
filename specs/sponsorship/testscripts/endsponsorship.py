#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import stellar_sdk
from stellar_sdk.transaction_builder import Keypair
import click

@click.command()
@click.argument("activatorsecret", type=str)
@click.argument("sponsoredaccount", type=str)
def end_sponsorship(activatorsecret,sponsoredaccount):
    activator_kp=Keypair.from_secret(activatorsecret)

    horizon_server = stellar_sdk.Server()

    source_account = horizon_server.load_account(activator_kp.public_key)

    base_fee = horizon_server.fetch_base_fee()
    transaction = (
        stellar_sdk.TransactionBuilder(
            source_account=source_account,
            network_passphrase=stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
        .append_revoke_account_sponsorship_op(sponsoredaccount)
        .build()
    )
    transaction.sign(activator_kp)
    horizon_server.submit_transaction(transaction)
    print(f"Stopped sponsoring account {sponsoredaccount }")


if __name__ == "__main__":
    end_sponsorship()