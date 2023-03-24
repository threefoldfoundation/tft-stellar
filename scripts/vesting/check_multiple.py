#!/usr/bin/env python
# pylint: disable=no-value-for-parameter
import click
import os
import sys

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../../lib/stats/")
from stats import get_vesting_accounts


@click.command(help="Checks if there are multiple vesting accounts for a single owner account")
@click.option("--network", type=click.Choice(["test", "public"], case_sensitive=False), default="public")
def check_multiple(network):

    vesting_accounts = get_vesting_accounts(network, "TFT")

    owners=[]
    owners_with_multiple_vesting_accounts=[]
    for vesting_account in vesting_accounts:
        owner=vesting_account['owner']
        if owner in owners:
            if not owner in owners_with_multiple_vesting_accounts:
                owners_with_multiple_vesting_accounts.append(owner)
                continue
        owners.append(owner)
        
    if len(owners_with_multiple_vesting_accounts)==0:
        print("There are no owners with multiple vesting accounts")
    else:
       print("Owners with multiple vesting accounts:") 
    for owner in owners_with_multiple_vesting_accounts:
        print(owner)


if __name__ == "__main__":
    check_multiple()
