#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
from decimal import Decimal
import time
import math
from datetime import datetime
from tfchainbalances import unlockhash_get
import stellar_sdk
import requests


def stellar_address_to_tfchain_address(stellar_address):
    from tfchaintypes.CryptoTypes import PublicKey, PublicKeySpecifier
    from stellar_sdk import strkey

    raw_public_key = strkey.StrKey.decode_ed25519_public_key(stellar_address)
    rivine_public_key = PublicKey(PublicKeySpecifier.ED25519, raw_public_key)
    return str(rivine_public_key.unlockhash)


@click.command(help="Find the stellar addresses from a list of tfchain addresses")
@click.argument("tfchainaddressesfile", default="tfchainaddresses.txt", type=click.File("r"))
@click.argument("alternativematchfile", default="matched.txt", type=click.File("r"))
@click.argument("deauthorizationsfile", default="deauthorizations.txt", type=click.File("r"))
@click.argument("issuedfile", default="issued.txt", type=click.File("r"))
def find_command(tfchainaddressesfile, alternativematchfile, deauthorizationsfile, issuedfile):
    alternativematches = {}
    for alternativematchline in alternativematchfile.read().splitlines():
        splitline = alternativematchline.split()
        alternativematches[splitline[0]] = splitline[1]
    deauthorizations={}
    for deauthorization in deauthorizationsfile.read().splitlines():
        splitdeauthorization = deauthorization.split()
        deauthorizations[splitdeauthorization[1]]=splitdeauthorization[0]
    issuances={}
    for issuance in issuedfile.read().splitlines():
            splitissuance = issuance.split()
            issuance_perdeauthorization=issuances.get(splitissuance[0],[])
            issuance_perdeauthorization.append(splitissuance[3]) #append the address
            issuances[splitissuance[0]]=issuance_perdeauthorization

    for tfchainaddress in tfchainaddressesfile.read().splitlines():
        mainstellaraddress = alternativematches.get(tfchainaddress)
        deauthorizationtx = deauthorizations.get(tfchainaddress)
        if deauthorizationtx in issuances:
            mainstellaraddress= "TFT issued but not to the normal addresss"
            for address in issuances[deauthorizationtx]:
                if tfchainaddress == stellar_address_to_tfchain_address(address):
                    mainstellaraddress = address
                    break

        print(f"tfchainaddress: {tfchainaddress}, deauthtx:{deauthorizationtx}, Stellar address: {mainstellaraddress}")


if __name__ == "__main__":
    find_command()
