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


@click.command(help="Exports the data from the vestingdashboard")
def export():
    for modelname in vesting_entry_model.list_all():
        print(json.dumps(vesting_entry_model.get(modelname).to_dict()))


if __name__ == "__main__":
    export()