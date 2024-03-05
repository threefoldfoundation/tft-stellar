#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
from decimal import Decimal


@click.command(help="Conversion checks")
@click.argument("deauthorizationsfile", default="deauthorizations.txt", type=click.File("r"))
@click.argument("deauthorizedbalancesfile", default="deauthorizedbalances.txt", type=click.File("r"))
@click.argument("issuedfile", default="issued.txt", type=click.File("r"))
def check_command(deauthorizationsfile, deauthorizedbalancesfile, issuedfile):

    deauthorizedbalances = {}
    for deauthorizedbalance in deauthorizedbalancesfile.read().splitlines():
        splitbalance = deauthorizedbalance.split()
        deauthorizedbalances[splitbalance[0]] = {"free": splitbalance[1], "locked": splitbalance[2]}

    deauthorizations = {}
    numberofdeauthorizations = 0
    numberofzerobalances = 0
    # total_stellar = Decimal()
    total_rivine = Decimal()
    migrated_to_stellar = Decimal()
    for deauthorization in deauthorizationsfile.read().splitlines():
        numberofdeauthorizations += 1
        splitdeauthorization = deauthorization.split()
        deauthorizationtx = splitdeauthorization[0]
        tfchainaddress = splitdeauthorization[1]
        if tfchainaddress in deauthorizedbalances:
            balance = deauthorizedbalances[tfchainaddress]
            if balance["free"] == "0" and balance["locked"] == "0":
                numberofzerobalances += 1
                continue
        deauthorizations[deauthorizationtx] = tfchainaddress
    print(f"{numberofdeauthorizations} tfchain addresses are deauthorized")
    print(f"{numberofzerobalances} had 0 TFT and do not have to be migrated")

    issuedtokens = {}
    for issuance in issuedfile.read().splitlines():
        splitissuance = issuance.split()
        deauthorizationtx = splitissuance[0]
        totalissuedamount = Decimal(splitissuance[1])
        # all issued tokens on stellar that have a hash type memo
        # total_stellar += totalissuedamount
        if deauthorizationtx in issuedtokens:
            totalissuedamount += issuedtokens[deauthorizationtx]
        issuedtokens[deauthorizationtx] = totalissuedamount

    numberofcorrectconversions = 0
    numberofincorrectconversions = 0
    incorrectconversions = []
    for deauthorizationtx, issuedbalance in issuedtokens.items():
        if deauthorizationtx not in deauthorizations:
            continue
        tfchainaddress = deauthorizations.pop(deauthorizationtx)
        freedeauthorized = Decimal(deauthorizedbalances[tfchainaddress]["free"])
        lockeddeauthorized = Decimal(deauthorizedbalances[tfchainaddress]["locked"])
        deauthorizedbalance = Decimal("{0:.7f}".format(freedeauthorized)) + Decimal(
            "{0:.7f}".format(lockeddeauthorized)
        )
        difference = issuedbalance - deauthorizedbalance
        # if the differens is less than 1 tft, assume arounding error
        if difference > Decimal("-1") and difference < Decimal("1"):
            numberofcorrectconversions += 1
        else:
            incorrectconversions.append(
                f"deauthtx: {deauthorizationtx} tfchainaddress: {tfchainaddress} difference: {difference}"
            )
            numberofincorrectconversions += 1
        # all de-authorized balance on rivine
        total_rivine += deauthorizedbalance
        # migrated balance
        migrated_to_stellar += issuedbalance

    conversionsleft = len(deauthorizations)
    print(f"{numberofdeauthorizations-(conversionsleft+numberofzerobalances)} conversions done, {conversionsleft} left")
    print()
    print(f"{total_rivine} TFT is the sum of all deauthorized balances on rivine")
    print(f"{migrated_to_stellar} TFT was migrated from rivine to stellar (hash memo match deauth tx on rivine)")
    print(f"{(total_rivine - migrated_to_stellar)} TFT Remains on rivine unmigrated (based on above number)")
    print()
    print(f"{numberofcorrectconversions} correct conversions")
    print(f"{numberofincorrectconversions} incorrect conversions:")
    for ic in incorrectconversions:
        print(ic)


if __name__ == "__main__":
    check_command()
