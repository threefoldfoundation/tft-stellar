#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import time
import click
import stellar_sdk
import math
from stellar_sdk.transaction_builder import TransactionBuilder
import sys

sys.path.append("..")
from common.addTrustlines import add_trustline
from common.createAccounts import create_keypair, activate_account
from common.fundWithAsset import send_asset_to_account


def set_account_signers(address, public_key_signer, preauth_tx_hash, signer_kp):
    horizon_server = stellar_sdk.Server()
    account = horizon_server.load_account(address)
    tx = (
        TransactionBuilder(account)
        .append_pre_auth_tx_signer(preauth_tx_hash, 1)
        .append_ed25519_public_key_signer(public_key_signer, 1)
        .append_set_options_op(master_weight=1, low_threshold=2, med_threshold=2, high_threshold=2)
        .build()
    )

    tx.sign(signer_kp)
    response = horizon_server.submit_transaction(tx)
    print(response)
    print(
        "Set the signers of {address} to {pk_signer} and {preauth_hash_signer}".format(
            address=address, pk_signer=public_key_signer, preauth_hash_signer=preauth_tx_hash
        )
    )


def create_preauth_transaction(escrow_kp):
    unlock_time = int(time.time()) + 60 * 10  # 10 minutes from now
    horizon_server = stellar_sdk.Server()
    escrow_account = horizon_server.load_account(escrow_kp.public_key)
    escrow_account.increment_sequence_number()
    tx = (
        TransactionBuilder(escrow_account)
        .append_set_options_op(master_weight=0, low_threshold=1, med_threshold=1, high_threshold=1)
        .add_time_bounds(unlock_time, 0)
        .build()
    )
    tx.sign(escrow_kp)
    return tx


@click.command()
@click.argument("from_secret", type=str)
@click.argument("destination", type=str)
@click.option("--asset", type=str, default="TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3")
@click.option("--amount", type=str, default="1")
def send_locked_funds(from_secret, destination, asset, amount):
    from_kp = stellar_sdk.Keypair.from_secret(from_secret)
    split_asset = asset.split(":", 1)
    asset_code = split_asset[0]
    asset_issuer = split_asset[1]
    print(
        "Sending {amount} {asset} from {from_address} to {destination}".format(
            amount=amount, asset=asset, from_address=from_kp.public_key, destination=destination
        )
    )

    print("Creating  escrow account")
    escrow_kp = create_keypair()
    # minimum account balance as described at https://www.stellar.org/developers/guides/concepts/fees.html#minimum-account-balance
    horizon_server = stellar_sdk.Server()
    base_fee = horizon_server.fetch_base_fee()
    base_reserve = 0.5
    minimum_account_balance = (2 + 1 + 3) * base_reserve  # 1 trustline and 3 signers
    required_XLM = minimum_account_balance + base_fee * 0.0000001 * 3
    activate_account(escrow_kp.public_key, from_kp, math.ceil(required_XLM))
    add_trustline(escrow_kp.secret, asset_code, asset_issuer)

    preauth_tx = create_preauth_transaction(escrow_kp)
    preauth_tx_hash = preauth_tx.hash()

    set_account_signers(escrow_kp.public_key, destination, preauth_tx_hash, escrow_kp)
    print("Unlock Transaction:")
    print(preauth_tx.to_xdr())

    send_asset_to_account(escrow_kp.public_key, asset, amount, from_kp.public_key, (from_secret,))


if __name__ == "__main__":
    send_locked_funds()
