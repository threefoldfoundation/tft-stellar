#!/usr/bin/env python
# pylint: disable=no-value-for-parameter
import click
import os
import sys
import stellar_sdk

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../../lib/stats/")
from stats import get_vesting_accounts


DATA_ENTRY_KEY = "tft-vesting"


@click.command(help="Create unvesting transactions for TFT vesting accounts")
@click.argument("transactionsfile", default="unvesting_transactions.txt", type=click.File("w"))
@click.option("--network", type=click.Choice(["test", "public"], case_sensitive=True), default="public")
def create_unvesting_transactions(transactionsfile, network):

    tft_asset = stellar_sdk.Asset(
        "TFT",
        "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3"
        if network == "test"
        else "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
    )
    vesting_accounts = get_vesting_accounts(network, "TFT")

    for vesting_account in vesting_accounts:
        # TODO: maybe check if it is a real vesting account, the stats lib does not do a thorough check
        print(
            f"{vesting_account['account']} with owner {vesting_account['owner']} has {vesting_account['amount']} TFT'"
        )
        horizon_server = (
            stellar_sdk.Server() if network == "test" else stellar_sdk.Server("https://horizon.stellar.org")
        )
        account = horizon_server.load_account(vesting_account["account"])
        txb = stellar_sdk.TransactionBuilder(
            account,
            stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
            if network == "test"
            else stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE,
        )
        txb.append_payment_op(destination=vesting_account["owner"], asset=tft_asset, amount=vesting_account["amount"])
        txb.append_change_trust_op(tft_asset, "0")
        txb.append_manage_data_op(DATA_ENTRY_KEY, None)
        txb.append_account_merge_op(destination=vesting_account["owner"])
        tx_envelope = txb.build()
        # increase the max transaction fee to 0.099 xlm
        tx_envelope.transaction.fee = 990000
        tx_xdr = tx_envelope.to_xdr()
        transactionsfile.write(f"{tx_xdr}\n")


if __name__ == "__main__":
    create_unvesting_transactions()
