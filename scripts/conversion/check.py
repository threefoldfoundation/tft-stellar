#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click


@click.command(help="Conversion checks")
@click.argument("deauthorizationsfile", default="deauthorizations.txt", type=click.File("r"))
@click.argument("deauthorizedbalancesfile", default="deauthorizedbalances.txt", type=click.File("r"))
@click.argument("issuedfile", default="issued.txt", type=click.File("r"))
def check_command(deauthorizationsfile,deauthorizedbalancesfile, issuedfile):
    
    
    deauthorizedbalances={}
    for deauthorizedbalance in deauthorizedbalancesfile.read().splitlines():
        splitbalance=deauthorizedbalance.split()
        deauthorizedbalances[splitbalance[0]]={'free':splitbalance[2],'locked':splitbalance[4]}
    
    deauthorizations = {}
    numberofdeauthorizations=0
    numberofzerobalances=0
    for deauthorization in deauthorizationsfile.read().splitlines():
        numberofdeauthorizations+=1
        splitdeauthorization = deauthorization.split()
        deauthorizationtx=splitdeauthorization[0]
        tfchainaddress=splitdeauthorization[1]
        if tfchainaddress in deauthorizedbalances:
            balance= deauthorizedbalances[tfchainaddress] 
            if balance['free']=='0' and balance['locked']=='0':
                numberofzerobalances+=1
                continue
        deauthorizations[deauthorizationtx] =tfchainaddress 
    print(f"{numberofdeauthorizations} tfchain addresses are deauthorized")
    print(f"{numberofzerobalances} had 0 TFT  and do not have to be migrated")

    for issuance in issuedfile.read().splitlines():
        splitissuance = issuance.split()
        deauthorizationtx=splitissuance[0]
        if deauthorizationtx in deauthorizations:
            del deauthorizations[deauthorizationtx]
    conversionsleft = len(deauthorizations)
    print(f"{numberofdeauthorizations-(conversionsleft+numberofzerobalances)} conversions done, {conversionsleft} left")


if __name__ == "__main__":
    check_command()
