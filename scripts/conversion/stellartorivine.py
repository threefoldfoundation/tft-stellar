#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
import os
import sys

CURRENT_FULL_PATH = os.path.dirname(os.path.abspath(__file__))
lib_path = CURRENT_FULL_PATH + "/../../lib/"
sys.path.append(lib_path)
import tfchaintypes

FULL_ASSETCODES = {
    "TFT": "TFT:GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
    "TFTA": "TFTA:GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2",
}


def stellar_address_to_tfchain_address(stellar_address):
    from tfchaintypes.CryptoTypes import PublicKey, PublicKeySpecifier
    from stellar_sdk import strkey

    raw_public_key = strkey.StrKey.decode_ed25519_public_key(stellar_address)
    rivine_public_key = PublicKey(PublicKeySpecifier.ED25519, raw_public_key)
    return str(rivine_public_key.unlockhash)



@click.command(help="Find the rivine addres from a Stellar address")
@click.argument("stellaraddress", type=str, required=True)
def command(stellaraddress):
            tfchainaddress = stellar_address_to_tfchain_address(stellaraddress)
            print(f"{tfchainaddress}")
 


if __name__ == "__main__":
    command()
