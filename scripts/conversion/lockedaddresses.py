#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
import requests
import json
import time
import sys
import faulthandler

TFCHAIN_EXPLORER = "https://explorer2.threefoldtoken.com"


@click.command(help="List locked tfchain addresses with the locking transaction")
@click.option("--startingheight",default=-1,type=int)
def list_locked_addresses(startingheight):
    currentheight=startingheight
    if currentheight<=0:
        response = requests.get(TFCHAIN_EXPLORER + "/explorer")
        j = response.json()
        currentheight = j["height"]

    while currentheight > 500000:
        print(currentheight,file=sys.stderr)
        try:
            response = requests.get(TFCHAIN_EXPLORER + f"/explorer/blocks/{currentheight}")
        except requests.exceptions.ConnectionError as e:
            print (e, file=sys.stderr)
            time.sleep(2)
            continue
        j = response.json()
        for transaction in j["block"]["transactions"]:
            if transaction["rawtransaction"]["version"] != 176:
                continue
            for address in transaction["rawtransaction"]["data"]["deauthaddresses"]:
                print(f"{transaction['id']} {address}")
        time.sleep(1)
        currentheight -= 1


if __name__ == "__main__":
    faulthandler.enable()
    list_locked_addresses()
