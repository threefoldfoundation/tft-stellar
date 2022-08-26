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


def get_escrowaccount_unlocktime(address):
    horizon_server = stellar_sdk.Server("https://horizon.stellar.org")
    accounts_endpoint = horizon_server.accounts()
    accounts_endpoint.account_id(address)

    response = accounts_endpoint.call()
    preauth_signer = [signer["key"] for signer in response["signers"] if signer["type"] == "preauth_tx"][0]
    resp = requests.post(
        "https://tokenservices.threefold.io/threefoldfoundation/unlock_service/get_unlockhash_transaction",
        json={"args": {"unlockhash": preauth_signer}},
    )
    resp.raise_for_status()

    txe = stellar_sdk.TransactionEnvelope.from_xdr(
        resp.json()["transaction_xdr"], stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE
    )
    tx = txe.transaction
    if tx.time_bounds is not None:
        return tx.time_bounds.min_time


@click.command(help="Conversion check for a single tfchain address")
@click.argument("tfchainaddress", type=str, required=True)
@click.argument("deauthorizationsfile", default="deauthorizations.txt", type=click.File("r"))
@click.argument("issuedfile", default="issued.txt", type=click.File("r"))
@click.option("--stellaraddress", default="", type=str)
def check_command(tfchainaddress, deauthorizationsfile, issuedfile, stellaraddress):
    if stellaraddress:
        if tfchainaddress != stellar_address_to_tfchain_address(stellaraddress):
            print("Warning: The tfchain address does not match the stellar adress")

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
    mainstellaraddress = stellaraddress
    for issuance in issuedfile.read().splitlines():
        splitissuance = issuance.split()
        if deauthorizationtx != splitissuance[0]:
            continue
        amount = Decimal(splitissuance[1])
        tokencode = splitissuance[2]
        address = splitissuance[3]
        totalissuedamount += amount
        if (tfchainaddress == stellar_address_to_tfchain_address(address)) or (address == mainstellaraddress):
            mainstellaraddress = address
            totalfreeissued += amount
            issuedtokens.append(f"{amount} {tokencode} {address} Free")
        else:
            totallockedissued += amount
            try:
                unlocktime = get_escrowaccount_unlocktime(address)
                issuedtokens.append(f"{amount} {tokencode} {address} Locked {unlocktime}")
            except (stellar_sdk.exceptions.NotFoundError, IndexError):
                issuedtokens.append(f"{amount} {tokencode} {address} already unlocked")

    print(f"Stellar wallet address: {mainstellaraddress}")

    unlockhash = unlockhash_get(tfchainaddress)
    balance = unlockhash.balance()

    unlocked_tokens = Decimal("{0:.7f}".format(balance.available.value))
    locked_tokens = balance.locked.value
    print(f"Tfchain TFT: {unlocked_tokens+locked_tokens} Free: {unlocked_tokens} Locked: {locked_tokens}")
    print(f"Tokens issued: {totalissuedamount} Free: {totalfreeissued} Locked: {totallockedissued}")

    # Generate list of locked tokens that should have been issued
    lockedshouldhavebeenissued = []
    totalockedamountthatshouldhavebeenisssued = Decimal()
    for tx in unlockhash.transactions:
        for coin_output in tx.coin_outputs:
            if str(coin_output.condition.unlockhash) != tfchainaddress:
                continue
            lock_time = coin_output.condition.lock.value
            if lock_time == 0:
                continue
            asset = "TFT"
            if time.time() < lock_time:
                amount = Decimal("{0:.7f}".format(coin_output.value.value))
                totalockedamountthatshouldhavebeenisssued += amount
                lockedshouldhavebeenissued.append(f"{amount} {asset} {math.ceil(lock_time)}")

    print(f"Locked tokens that should have been issued ({totalockedamountthatshouldhavebeenisssued}):")
    for should in lockedshouldhavebeenissued:
        print(should)

    missingissuances = lockedshouldhavebeenissued
    toomuchissued = []

    print("Isuances:")
    for issuance in issuedtokens:
        print(f"{issuance}")
        splitissuance = issuance.split()
        if splitissuance[3] == "Free":
            continue
        formattedissuance = f"{Decimal(splitissuance[0]):.7f} {splitissuance[1]} {splitissuance[4]}"
        if formattedissuance in missingissuances:
            missingissuances.remove(formattedissuance)
        else:
            toomuchissued.append(formattedissuance)

    totaltoomuchissued = Decimal()
    for issuance in toomuchissued:
        splitissuance = issuance.split()
        totaltoomuchissued += Decimal(splitissuance[0])

    print(f"Too much issued: {totaltoomuchissued} locked tokens:")
    for issuance in toomuchissued:
        issuancetime = int(issuance.split()[2])
        print(f"{issuance} {datetime.fromtimestamp(issuancetime)}")

    totalmissingissuances = Decimal()
    for issuance in missingissuances:
        splitissuance = issuance.split()
        totalmissingissuances += Decimal(splitissuance[0])

    print(f"Missing issuances: {totalmissingissuances} tokens:")
    for issuance in missingissuances:
        print(issuance)

    print("Correction script:")
    print(f"deauthtxid='{deauthorizationtx}'")
    if unlocked_tokens != totalfreeissued:
        asset = FULL_ASSETCODES["TFT"]
        issuer_address = asset.split(":")[1]
        print(
            f"conversionwallet.transfer('{mainstellaraddress}','{unlocked_tokens}',asset='{asset}', memo_hash=deauthtxid,fund_transaction=False,from_address='{issuer_address}')"
        )

    for issuance in missingissuances:
        splitissuance = issuance.split()
        amount = splitissuance[0]
        tokencode = splitissuance[1]
        lockedtime = splitissuance[2]
        asset = FULL_ASSETCODES[tokencode]
        issuer_address = asset.split(":")[1]
        print(
            f"conversionwallet.transfer('{mainstellaraddress}','{amount}',asset='{asset}',locked_until={lockedtime}, memo_hash=deauthtxid,fund_transaction=False,from_address='{issuer_address}')"
        )


if __name__ == "__main__":
    check_command()
