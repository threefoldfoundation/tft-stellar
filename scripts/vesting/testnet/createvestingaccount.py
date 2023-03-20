#!/usr/bin/env python
# pylint: disable=no-value-for-parameter
import click
import stellar_sdk
import requests


DATA_ENTRY_KEY = "tft-vesting"
VESTING_SCHEME = "month1=05/2021,48months,priceunlock=tftvalue>month*0.015+0.15"

_COSIGNERS = [
    "GBOZV7I3NJGXIFBMGHTETCY7ZL36QMER25IJGRFEEX3KM36YRUMHEZAP",
    "GCU5OGRCFJ3NWQWUF3A4MAGNYABOPJMCHMXYQ7TC4RQ6IYBIZBEOGN6H",
    "GAK2Q3P3YOAPK6MCM4P3ASDJYSHQ376LIO64CHBXNKIRFZECH2JY2LYX",
    "GALOCGHPJ2KQ67VIZRSLOAPJIBCUL54WG6ZHFDB6AKPIMEQXHU374UCJ",
    "GC3IFIJ7KEOZ5CUZS57HMLJLXISS7N45INIGXO2JFNJBLKOGYTSADFPB",
    "GD56QGOWI5ZRJAXNLMAH6BQ3MQEXNWI5H6Q57BFMOQZKPMRLPIYK4RC6",
    "GAJFU5JCWRVJ5G7HDYSW6NMDSS6XTRPCNEULD5MWCKQEIGFFSJMDZXUA",
    "GDBDJCWCEHLCCJ74HJUDJIBTZO7JVFCI2IIDLEPL33FHOAKVDCNAUE4P",
    "GBMXLD4BEJWWETPCFTO2NI7MFRGGBFZDIOVA7OHHFA5XBTB7YHUQBQME",
]


def _get_horizon_server() -> stellar_sdk.Server:
    return stellar_sdk.Server()


def _is_multisig_account(address: str) -> bool:
    horizon_server = _get_horizon_server()
    resp = horizon_server.accounts().account_id(address).call()
    return len(resp["signers"]) != 1


def _create_recovery_transaction(vesting_address: str, activation_account_id: str) -> stellar_sdk.TransactionEnvelope:
    horizon_server = _get_horizon_server()
    source_account = horizon_server.load_account(vesting_address)
    source_account.sequence += 1
    tx = stellar_sdk.TransactionBuilder(source_account)
    tftasset = stellar_sdk.Asset("TFT", "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3")
    tx.append_change_trust_op(tftasset, limit="0")
    tx.append_manage_data_op(DATA_ENTRY_KEY, None)
    tx.append_account_merge_op(activation_account_id)
    txe = tx.build()

    # save the preauth transaction in our unlock service
    unlock_hash_signer = stellar_sdk.strkey.StrKey.encode_pre_auth_tx(txe.hash())
    data = {"unlockhash": unlock_hash_signer, "transaction_xdr": txe.to_xdr()}
    url = f"https://testnet.threefold.io/threefoldfoundation/unlock_service/create_unlockhash_transaction"
    resp = requests.post(url, json={"args": data})
    resp.raise_for_status()
    return txe


def _create_vesting_account(owner_address, activationaccount_secret: str) -> str:

    if _is_multisig_account(owner_address):
        raise Exception("Multisig accounts are not supported")

    escrow_kp = stellar_sdk.Keypair.random()
    escrow_address = escrow_kp.public_key
    activation_account_kp = stellar_sdk.Keypair.from_secret(activationaccount_secret)

    horizon_server = _get_horizon_server()

    activation_account = horizon_server.load_account(activation_account_kp)

    tftasset = stellar_sdk.Asset("TFT", "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3")

    txb = (
        stellar_sdk.TransactionBuilder(activation_account)
        .append_create_account_op(escrow_address, starting_balance="7.6")
        .append_change_trust_op(tftasset, source=escrow_address)
    )

    tx = txb.build()
    tx.sign(activation_account_kp)
    tx.sign(escrow_kp)
    horizon_server.submit_transaction(tx)
    vesting_account = horizon_server.load_account(escrow_address)
    txb = stellar_sdk.TransactionBuilder(
        vesting_account, network_passphrase=stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
    ).append_ed25519_public_key_signer(owner_address, weight=5, source=escrow_address)
    recovery_transaction = _create_recovery_transaction(escrow_address, activation_account_kp.public_key)

    txb.append_pre_auth_tx_signer(recovery_transaction.hash(), weight=10, source=escrow_address)
    for cosigner in _COSIGNERS:
        txb.append_ed25519_public_key_signer(cosigner, weight=1, source=escrow_address)
    txb.append_manage_data_op(DATA_ENTRY_KEY, VESTING_SCHEME, source=escrow_address)
    txb.append_set_options_op(
        master_weight=0, low_threshold=10, med_threshold=10, high_threshold=10, source=escrow_address
    )

    tx = txb.build()
    tx.sign(escrow_kp)
    horizon_server.submit_transaction(tx)
    return escrow_address


@click.command(help="Create a vesting account on testnet")
@click.argument("owner_address", type=str, required=True)
@click.argument("activationaccount_secret", type=str, required=True)
def create_vesting_account(owner_address: str, activationaccount_secret: str):
    escrow_address = _create_vesting_account(owner_address, activationaccount_secret)
    print(f"Vesting account with escrow address: {escrow_address}")


if __name__ == "__main__":
    create_vesting_account()
