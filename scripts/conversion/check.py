#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click


@click.command(help="Conversion checks")
@click.argument("deauthorizationsfile", default="deauthorizations.txt", type=click.File("r"))
@click.argument("issuedfile", default="issued.txt", type=click.File("r"))
def check_command(deauthorizationsfile, issuedfile):
    deauthorizations = {}
    for deauthorization in deauthorizationsfile.read().splitlines():
        splitdeauthorization = deauthorization.split()
        deauthorizations[splitdeauthorization[0]] = splitdeauthorization[1]
    numberofdeauthorizations = len(deauthorizations)
    print(f"{numberofdeauthorizations} tfchain addresses deauthorized")
    for issuance in issuedfile.read().splitlines():
        splitissuance = issuance.split()
        if splitissuance[0] in deauthorizations:
            del deauthorizations[splitissuance[0]]
    conversionsleft = len(deauthorizations)
    print(f"{numberofdeauthorizations-conversionsleft} conversions done, {conversionsleft} left")


if __name__ == "__main__":
    check_command()
