#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
from decimal import Decimal


@click.command(help="Conversion check for a sibgle tfchain address")
@click.argument("tfchainaddress",type=str,required=True)
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
    totalissuedamount=Decimal()
    for issuance in issuedfile.read().splitlines():
        splitissuance = issuance.split()
        if deauthorizationtx != splitissuance[0]:
            continue
        totalissuedamount += Decimal(splitissuance[1])
        issuedtokens.append(issuance)

    print(f"{totalissuedamount} tokens issued")
    for issuance in issuedtokens:
        print(issuance)

if __name__ == "__main__":
    check_command()
