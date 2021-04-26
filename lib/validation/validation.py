#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

from jumpscale.loader import j
import click
import stellar_sdk
import datetime

from urllib import parse


_ASSET_ISUERS = {
    "test": {
        "TFT": "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3",
        "TFTA": "GB55A4RR4G2MIORJTQA4L6FENZU7K4W7ATGY6YOT2CW47M5SZYGYKSCT",
    },
    "public": {
        "TFT": "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
        "TFTA": "GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2",
    },
}
_HORIZON_NETWORKS = {"test": "https://horizon-testnet.stellar.org", "public": "https://horizon.stellar.org"}
_THREEFOLDFOUNDATION_TFTSTELLAR_SERVICES = {"test": "testnet.threefold.io", "public": "tokenservices.threefold.io"}

TFCHAIN_EXPLORER = "https://explorer2.threefoldtoken.com"


class TokenDestruction(object):
    def __init__(self, asset_code, asset_issuer, amount, sender):
        self.asset_code = asset_code
        self.asset_issuer = asset_issuer
        self.amount = amount
        self.sender = sender


def validate(transaction_hash, network):
    horizon_server = stellar_sdk.Server(_HORIZON_NETWORKS[network])
    tokendestructions = []
    issuer = _ASSET_ISUERS[network]["TFTA"]
    try:
        response = horizon_server.payments().for_transaction(transaction_hash).limit(100).call()
        payments = response["_embedded"]["records"]
        for payment in payments:
            if payment["to"] != _ASSET_ISUERS[network]["TFTA"]:
                continue
            if payment["type"] != "payment":
                continue
            if payment["asset_type"] == "native":
                continue
            if payment["asset_code"] != "TFTA" or payment["asset_issuer"] != issuer:
                continue
            amount = payment["amount"]
            sender = payment["from"]
            tokendestructions.append(TokenDestruction("TFTA", issuer, amount, sender))
    except stellar_sdk.exceptions.BadRequestError as e:
        if not "invalid_field" in e.extras:
            raise e
    return tokendestructions


@click.command(help="Conversion check for a single tfchain address")
@click.argument("transaction_hash", type=str, required=True)
@click.option("--network", type=click.Choice(["test", "public"], case_sensitive=False), default="public")
def validate_command(transaction_hash, network):
    # Check if it's a TFTA destruction
    tokendestructions = validate(transaction_hash, network)
    if not tokendestructions:
        print("Not a TFTA destruction")
    for d in tokendestructions:
        print(f"{d.sender} destroyed {d.amount} TFTA")
    # Check if it's a tfchain deauthorization

    pass


if __name__ == "__main__":
    validate_command()
