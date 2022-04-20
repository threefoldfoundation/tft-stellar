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
sys.path.append(current_full_path + "/../lib/stats/")
from stats import get_locked_accounts


@click.command(help="Lists information about timelocked TFT (owner account, TFT, escrow account)")
@click.option("--network", type=click.Choice(["test", "public"], case_sensitive=False), default="public")
def list_lockedTFT_info(network):

    locked_accounts, _ , _ = get_locked_accounts(network, "TFT",[])

    for escrow_account in locked_accounts:
        for signer in escrow_account["signers"]:
            if signer["type"]=="ed25519_public_key" and signer["key"]!=escrow_account['account']:
                owner_account=signer["key"]
        print(
            f"{owner_account},{escrow_account['amount']},{escrow_account['account']}"
        )


if __name__ == "__main__":
    list_lockedTFT_info()
