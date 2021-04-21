#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
import time, sys, os
import requests

CURRENT_FULL_PATH = os.path.dirname(os.path.abspath(__file__))
lib_path = CURRENT_FULL_PATH + "/../../lib/"
sys.path.append(lib_path)
from tfchainexplorer import unlockhash_get


@click.command(help="Get the balances before conversion for a list of addresses")
@click.argument("tfchainaddressesfile", default="tft_addresses.txt", type=click.File("r"))
def tfchain_balances(tfchainaddressesfile):
    counter = 0
    zerocounter = 0
    blockchaininfo = blockchain_info_get()
    for tfchainaddressline in tfchainaddressesfile.read().splitlines():
        tfchainaddress = tfchainaddressline.split()[0]
        counter += 1
        time.sleep(1)  # give the explorer a break
        unlockhash = unlockhash_get(tfchainaddress)
        if unlockhash is None:
            zerocounter += 1
            continue
        balance = unlockhash.balance(blockchaininfo)

        unlocked_tokens = balance.available.value
        locked_tokens = balance.locked.value

        if unlocked_tokens.is_zero() and locked_tokens.is_zero():
            zerocounter += 1
            continue
        print(f"{tfchainaddress} Free: {unlocked_tokens} Locked: {locked_tokens}")
    print(f"{zerocounter} of {counter} had a zero balance")


if __name__ == "__main__":
    tfchain_balances()
