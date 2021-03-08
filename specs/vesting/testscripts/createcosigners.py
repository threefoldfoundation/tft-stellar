#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import stellar_sdk
from stellar_sdk.transaction_builder import Keypair
import click
import json
import requests
from createaccount import create_activated_account


@click.command()
@click.argument("outputfile", default="cosigners.json", type=click.File(mode="w"))
def create_cosigners(outputfile):
    cosigners = []
    for i in range(9):
        cosigners.append(create_activated_account())
    json.dump(cosigners, outputfile, indent=4)


if __name__ == "__main__":
    create_cosigners()
