#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
from decimal import Decimal
import time
from datetime import datetime
from tfchainbalances import unlockhash_get


def stellar_address_to_tfchain_address(stellar_address):
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
    totalfreeissued = Decimal()
    totallockedissued = Decimal()
    mainstellaraddress = ""
    for issuance in issuedfile.read().splitlines():
        splitissuance = issuance.split()
        if deauthorizationtx != splitissuance[0]:
            continue
        amount = Decimal(splitissuance[1])
        tokencode = splitissuance[2]
        address = splitissuance[3]
        totalissuedamount += amount
        if tfchainaddress == stellar_address_to_tfchain_address(address):
            mainstellaraddress = address
            totalfreeissued += amount
        else:
            totallockedissued += amount
        issuedtokens.append(f"{amount} {tokencode} {address}")

    print(f"Stellar wallet address: {mainstellaraddress}")

    unlockhash = unlockhash_get(tfchainaddress)
    balance = unlockhash.balance()

    unlocked_tokens = Decimal("{0:.7f}".format(balance.available.value))
    locked_tokens = balance.locked.value
    print(f"Tfchain TFT: {unlocked_tokens+locked_tokens} Free: {unlocked_tokens} Locked: {locked_tokens}")
    print(f"Tokens issued: {totalissuedamount} Free: {totalfreeissued} Locked: {totallockedissued}")
    
    # Generate list of locked tokens that should have been issued
    lockedshouldhavebeenissued = []
    totalockedamountthatshouldhavebeenisssued=Decimal()
    for tx in unlockhash.transactions:
        for coin_output in tx.coin_outputs:
            lock_time = coin_output.condition.lock.value
            if lock_time == 0:
                break
            lock_time_date = datetime.fromtimestamp(lock_time)
            # if lock time year is before 2021 be convert to TFTA else we convert to TFT
            asset = "TFTA" if lock_time_date.year < 2021 else "TFT"
            if time.time() < lock_time:
                amount=Decimal("{0:.7f}".format(coin_output.value.value))
                totalockedamountthatshouldhavebeenisssued+=amount 
                lockedshouldhavebeenissued.append(f"{amount} {asset} {lock_time_date}")
    
    print(f"Locked tokens that should have been issued ({totalockedamountthatshouldhavebeenisssued}):")
    for should in lockedshouldhavebeenissued:
        print(should)
    
    print("Isuances:")
    for issuance in issuedtokens:
        splitissuance = issuance.split()
        print(f"{issuance} {'Free' if splitissuance[2]==mainstellaraddress else'Locked'}")
        
if __name__ == "__main__":
    check_command()
