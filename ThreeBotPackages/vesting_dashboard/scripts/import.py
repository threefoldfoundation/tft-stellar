#!/usr/bin/env python
# pylint: disable=no-value-for-parameter
import click
import os, sys
import json

from jumpscale.core.base import StoredFactory

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../models/")
from models import VestingEntry

vesting_entry_model = StoredFactory(VestingEntry)


@click.command(help="Imports the data from the vestingdashboard")
def import_data():
    for line in sys.stdin:
        data=json.loads(line)
        username=data["username"]
        owner_address=data["owner_address"]
        vesting_address=data["vesting_address"]
        _, vesting_check_count, _ = vesting_entry_model.find_many(
            f"{username}_{owner_address}", owner_address=owner_address
        )
        if vesting_check_count > 0:
            continue
        vesting_entry = vesting_entry_model.new(f"{username}_{owner_address}")
        vesting_entry.username = username
        vesting_entry.owner_address = owner_address
        vesting_entry.vesting_address = vesting_address
        vesting_entry.save()


if __name__ == "__main__":
    import_data()