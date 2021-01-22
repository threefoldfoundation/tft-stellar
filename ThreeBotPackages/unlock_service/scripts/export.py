#!/usr/bin/env python
# pylint: disable=no-value-for-parameter
import click
import stellar_sdk
import datetime
import os
import sys

from urllib import parse


current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../../../lib/stats/")
from stats import get_locked_accounts, get_unlockhash_transaction


@click.command(help="Exports the used unlocktransactions from the unlock service for TFT and TFTA")
@click.option("--network", type=click.Choice(["test", "public"], case_sensitive=False), default="public")
def export(network):
    for tokencode in ["TFT", "TFTA"]:

        locked_accounts = get_locked_accounts(network, tokencode)

        for locked_account in locked_accounts:
            print(get_unlockhash_transaction(network,locked_account["preauth_signers"][0]))

if __name__ == "__main__":
    export()
