#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import stellar_sdk
from stellar_sdk.transaction_builder import Keypair, TransactionBuilder
import click
import json
import requests
from createaccount import create_account

DATA_ENTRY_KEY="tft-vesting"

def create_recovery_transaction(vesting_address, asset_code:str, asset_issuer:str, activation_account:str)-> stellar_sdk.TransactionEnvelope:

    horizon_server = stellar_sdk.Server()
    source_account=horizon_server.load_account(vesting_address)
    source_account.sequence+=1
    txe=(TransactionBuilder(source_account,network_passphrase=stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE)
        .append_change_trust_op(asset_code=asset_code,asset_issuer=asset_issuer,limit="0")
        .append_manage_data_op(DATA_ENTRY_KEY,None)    
        .append_account_merge_op(activation_account)
        .build()
    )
    return txe


@click.command()
@click.argument("activationaccountsecret", type=str)
@click.argument("owneraddress", type=str)
@click.argument("cosignersfile", default="cosigners.json", type=click.File(mode="r"))
@click.option("--fullassetcode", default="TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3", type=str)
def create_escrow_account(activationaccountsecret, owneraddress, cosignersfile, fullassetcode):
    splitassetcode = fullassetcode.split(":")
    asset_code=splitassetcode[0]
    asset_issuer=splitassetcode[1]
    activation_kp = Keypair.from_secret(activationaccountsecret)

    horizon_server = stellar_sdk.Server()
    activation_account = horizon_server.load_account(activation_kp.public_key)

    new_escrow_account = create_account()
    escrow_address = new_escrow_account["address"]
    vesting_kp = Keypair.from_secret(new_escrow_account["secret"])
    txb = (
        TransactionBuilder(activation_account, network_passphrase=stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE)
        .append_create_account_op(escrow_address, starting_balance="7.6")
        .append_change_trust_op(asset_code, asset_issuer, source=escrow_address)
    )
    tx = txb.build()
    tx.sign(activation_kp)
    tx.sign(vesting_kp)
    horizon_server.submit_transaction(tx)
    vesting_account=horizon_server.load_account(escrow_address)
    txb = (
        TransactionBuilder(vesting_account, network_passphrase=stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE)
        .append_ed25519_public_key_signer(owneraddress, weight=5, source=escrow_address)
    )
    cosigners = json.load(cosignersfile)
    for cosigner in cosigners:
        txb.append_ed25519_public_key_signer(cosigner["address"], weight=1, source=escrow_address)
    txb.append_manage_data_op(DATA_ENTRY_KEY, "here comes the formula or reference", source=escrow_address)

    recovery_transaction=create_recovery_transaction(escrow_address,asset_code,asset_issuer, activation_kp.public_key)
    txb.append_pre_auth_tx_signer(recovery_transaction.hash(),weight=10,source=escrow_address)

    txb.append_set_options_op(
         master_weight=0, low_threshold=10, med_threshold=10, high_threshold=10, source=escrow_address
    )

    tx = txb.build()
    tx.sign(vesting_kp)
    horizon_server.submit_transaction(tx)
    print(f"Created escrow account {escrow_address}")
    print(f"Recovery transaction:\n{recovery_transaction.to_xdr()}")


if __name__ == "__main__":
    create_escrow_account()
