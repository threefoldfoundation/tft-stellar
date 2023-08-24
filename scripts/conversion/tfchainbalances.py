#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
import time, sys, os

CURRENT_FULL_PATH = os.path.dirname(os.path.abspath(__file__))
lib_path = CURRENT_FULL_PATH + "/../../lib/"
sys.path.append(lib_path)
from tfchainexplorer import unlockhash_get, blockchain_info_get


@click.command(help="Get the balances before conversion")
@click.argument("deauthorizationsfile", default="deauthorizations.txt", type=click.File("r"))
@click.argument("output", default="deauthorizedbalances.txt", type=click.File("w"))
def tfchain_balances(deauthorizationsfile, output):
    counter = 0
    blockchaininfo = blockchain_info_get()
    # Write header
    output.write('rivineaddress free locked total')
    for deauthorization in deauthorizationsfile.read().splitlines():
        counter += 1
        print(f"{counter}")
        splitdeauthorization = deauthorization.split()
        address = splitdeauthorization[1]
        unlockhash = unlockhash_get(address)
        balance = unlockhash.balance(blockchaininfo)
        unlocked_tokens = balance.available.value
        locked_tokens = balance.locked.value
        total= unlocked_tokens + locked_tokens 
        output.write(f"{address} {unlocked_tokens} {locked_tokens} {total}\n")
        time.sleep(2)  # give the explorer a break

if __name__ == "__main__":
    tfchain_balances()
