#!/usr/bin/env python
# pylint: disable=no-value-for-parameter
import click
import stellar_sdk
import datetime
import os
import sys
import requests
import json

from urllib import parse


current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../../lib/stats/")
from stats import get_vesting_accounts, get_unlockhash_transaction


@click.command(help="Lists the TFT vesting accounts")
@click.option("--network", type=click.Choice(["test", "public"], case_sensitive=False), default="public")
def list_vesting_accounts(network):

    vesting_accounts = get_vesting_accounts(network, "TFT")

    for vesting_account in vesting_accounts:
        print(f"{vesting_account['account']} has {vesting_account['amount']} TFT with vesting scheme '{vesting_account['scheme']}'")
        if len(vesting_account["preauth_signers"])==0:
            continue 
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


if __name__ == "__main__":
    list_vesting_accounts()
