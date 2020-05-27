#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
from decimal import Decimal


def stellar_address_to_tfchain_address( stellar_address):
    from tfchaintypes.CryptoTypes import PublicKey, PublicKeySpecifier
    from stellar_sdk import strkey

    raw_public_key = strkey.StrKey.decode_ed25519_public_key(stellar_address)
    rivine_public_key = PublicKey(PublicKeySpecifier.ED25519, raw_public_key)
    return str(rivine_public_key.unlockhash)


@click.command(help="Conversion check for a sibgle tfchain address")
@click.argument("tfchainaddress", type=str, required=True)
@click.argument("deauthorizationsfile", default="deauthorizations.txt", type=click.File("r"))
@click.argument("issuedfile", default="issued.txt", type=click.File("r"))
def check_command(tfchainaddress, deauthorizationsfile, issuedfile):

    deauthorizationtx = None
    for deauthorization in deauthorizationsfile.read().splitlines():
        splitdeauthorization = deauthorization.split()

        if tfchainaddress == splitdeauthorization[1]:
            deauthorizationtx = splitdeauthorization[0]
            break
    print(f"Deauthorization transaction: {deauthorizationtx}")

    issuedtokens = []
    totalissuedamount = Decimal()
    mainstellaraddress=""
    for issuance in issuedfile.read().splitlines():
        splitissuance = issuance.split()
        if deauthorizationtx != splitissuance[0]:
            continue
        amount = splitissuance[1]
        tokencode = splitissuance[2]
        address = splitissuance[3]
        if tfchainaddress==stellar_address_to_tfchain_address(address):
            mainstellaraddress=address
        totalissuedamount += Decimal(amount)
        issuedtokens.append(f"{amount} {tokencode} {address}")
    
    print(f"Stellar wallet address: {mainstellaraddress}")
    print(f"{totalissuedamount} tokens issued")
    for issuance in issuedtokens:
        print(issuance)


if __name__ == "__main__":
    check_command()
