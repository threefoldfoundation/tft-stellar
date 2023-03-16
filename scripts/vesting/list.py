#!/usr/bin/env python
# pylint: disable=no-value-for-parameter
import click
import os
import sys

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../../lib/stats/")
from stats import get_vesting_accounts 


@click.command(help="Lists the TFT vesting accounts")
@click.option("--network", type=click.Choice(["test", "public"], case_sensitive=False), default="public")
def list_vesting_accounts(network):

    vesting_accounts = get_vesting_accounts(network, "TFT")

    for vesting_account in vesting_accounts:
        print(
            f"{vesting_account['account']} has {vesting_account['amount']} TFT'"
        )


if __name__ == "__main__":
    list_vesting_accounts()
