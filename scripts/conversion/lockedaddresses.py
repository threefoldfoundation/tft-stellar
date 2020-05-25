#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
import requests
import json
import time

TFCHAIN_EXPLORER = "https://explorer2.threefoldtoken.com"


@click.command(help="List locked tfchain addresses with the locking transaction")
def list_locked_addresses():

    response = requests.get(TFCHAIN_EXPLORER + "/explorer")
    j = response.json()
    currentheight = j["height"]

    while currentheight > 500000:
        response = requests.get(TFCHAIN_EXPLORER + f"/explorer/blocks/{currentheight}")
        j = response.json()
        for transaction in j["block"]["transactions"]:
            if transaction["rawtransaction"]["version"] != 176:
                continue
            for address in transaction["rawtransaction"]["data"]["deauthaddresses"]:
                print(f"{transaction['id']} {address}")
        time.sleep(2)
        currentheight -= 1


if __name__ == "__main__":
    list_locked_addresses()
