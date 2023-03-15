#!/usr/bin/env python
# pylint: disable=no-value-for-parameter
import click
import stellar_sdk
import os
import sys
import requests
import json


current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../../../lib/stats/")
from stats import get_vesting_accounts, get_unlockhash_transaction


@click.command(help="Recoveresting accounts without TFT")
@click.option("--network", type=click.Choice(["test", "public"], case_sensitive=False), default="test")
def recover_empty_vesting_accounts(network):

    vesting_accounts = get_vesting_accounts(network, "TFT")

    for vesting_account in vesting_accounts:
        if vesting_account["amount"] != 0.0:
            continue
        if len(vesting_account["preauth_signers"]) == 0:
            continue

        print(f"Recovering empty vesting account {vesting_account['account']}")
        unlockhash = vesting_account["preauth_signers"][0]
        try:
            transaction = get_unlockhash_transaction(network, unlockhash)
            print(f"Clean up transaction:\n{json.dumps(transaction)}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(
                    f"Clean-up transaction with hash {unlockhash} for vesting account {vesting_account['account']} not found",
                    file=sys.stderr,
                )
        txe = stellar_sdk.transaction_envelope.TransactionEnvelope.from_xdr(
            transaction['transaction_xdr'] + "===",
            stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
            if network == "test"
            else stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE,
        )
        horizon_server = stellar_sdk.Server() if network == "test" else stellar_sdk.Server("https://horizon.stellar.org")
        horizon_server.submit_transaction(transaction_envelope=txe)


if __name__ == "__main__":
    recover_empty_vesting_accounts()
