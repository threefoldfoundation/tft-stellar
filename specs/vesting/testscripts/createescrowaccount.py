#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import stellar_sdk
from stellar_sdk.transaction_builder import Keypair, TransactionBuilder
import click
import json
import requests
from createaccount import create_account


@click.command()
@click.argument("activationaccountsecret", type=str)
@click.argument("owneraddress", type=str)
@click.argument("cosignersfile", default="cosigners.json", type=click.File(mode="r"))
@click.option("--fullassetcode", default="TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3", type=str)
def create_escrow_account(activationaccountsecret, owneraddress, cosignersfile, fullassetcode):
    splitassetcode = fullassetcode.split(":")
    activation_kp = Keypair.from_secret(activationaccountsecret)

    horizon_server = stellar_sdk.Server()
    activation_account = horizon_server.load_account(activation_kp.public_key)

    new_escrow_account = create_account()
    escrow_address = new_escrow_account["address"]
    escrow_kp = Keypair.from_secret(new_escrow_account["secret"])
    txb = (
        TransactionBuilder(activation_account, network_passphrase=stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE)
        .append_create_account_op(escrow_address, starting_balance="7.1")
        .append_change_trust_op(splitassetcode[0], splitassetcode[1], source=escrow_address)
        .append_ed25519_public_key_signer(owneraddress, weight=5, source=escrow_address)
    )
    cosigners = json.load(cosignersfile)
    for cosigner in cosigners:
        txb.append_ed25519_public_key_signer(cosigner["address"], weight=1, source=escrow_address)
    txb.append_manage_data_op("vesting","here comes the formula or reference", source=escrow_address)
    txb.append_set_options_op(
        master_weight=0, low_threshold=10, med_threshold=10, high_threshold=10, source=escrow_address
    )
    tx = txb.build()
    tx.sign(activation_kp)
    tx.sign(escrow_kp)
    horizon_server.submit_transaction(tx)

    print(f"Created escrow account {escrow_address}")


if __name__ == "__main__":
    create_escrow_account()
