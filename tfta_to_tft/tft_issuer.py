#!/usr/bin/env python
# pylint: disable=no-value-for-parameter
from jumpscale.loader import j
from jumpscale.clients.stellar.exceptions import NoTrustLine,TemporaryProblem

import jumpscale
import click
import time
import stellar_sdk
from requests.exceptions import ConnectionError


_ASSET_ISUERS = {
    "TEST": {
        "TFT": "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3",
        "TFTA": "GB55A4RR4G2MIORJTQA4L6FENZU7K4W7ATGY6YOT2CW47M5SZYGYKSCT",
    },
    "STD": {
        "TFT": "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
        "TFTA": "GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2",
    },
}

_HORIZON_NETWORKS = {"TEST": "https://horizon-testnet.stellar.org", "STD": "https://horizon.stellar.org"}

def fetch_new_transaction_memo_hashes(wallet, address, cursor):
    tx_list_result = wallet.list_transactions(address, cursor)
    tft_tx_memo_hashes = [tx.memo_hash_as_hex for tx in tx_list_result["transactions"] if tx.memo_hash is not None]
    return tft_tx_memo_hashes, tx_list_result["cursor"]


def already_issued_for_payment(payment_from_sales_service, issuer_memo_hashes):
    return payment_from_sales_service.transaction_hash in issuer_memo_hashes

def _get_horizon_server(network:str):
    server_url = _HORIZON_NETWORKS[network]
    return stellar_sdk.Server(horizon_url=server_url)

def fetch_new_payments_to_process(
    wallet, destination:str, cursor:str, asset, already_issued_memo_hashes, 
):
    payment_list_result = wallet.list_payments(destination, asset=asset, cursor=cursor)
    new_cursor = payment_list_result["cursor"]
    payments_to_process = []
    from_address_payments = [
        p for p in payment_list_result["payments"] if p.to_address == p.my_address
    ]
    for payment in from_address_payments:
        if not already_issued_for_payment(payment, already_issued_memo_hashes):
            payments_to_process.append(payment)
    return payments_to_process, new_cursor


@click.command(help="Convert burned TFTA's to TFT's")
@click.option("--walletname", type=str, default="tftatotftissuer")
@click.option("--preview/--no-preview",default=False)
def convert_tfta_to_tft(walletname,preview):
    wallet = j.clients.stellar.get(walletname)
    network = wallet.network.value
    print(f"Starting service to convert TFTA to TFT on the {network} network")

    tfta_issuer = _ASSET_ISUERS[network]["TFTA"]
    tft_issuer = _ASSET_ISUERS[network]["TFT"]

    tfta_payments_cursor = ""
    tft_transactions_cursor = ""

    tft_issuer_memo_hashes = []

    tft_tx_memo_hashes, tft_transactions_cursor = fetch_new_transaction_memo_hashes(
        wallet, tft_issuer, tft_transactions_cursor
    )
    tft_issuer_memo_hashes = [*tft_issuer_memo_hashes, *tft_tx_memo_hashes]


    payments_to_process,tfta_payments_cursor = fetch_new_payments_to_process(
        wallet,
        tfta_issuer,
        tfta_payments_cursor,
        f"TFTA:{tfta_issuer}",
        tft_issuer_memo_hashes,
    )

    while True:
        time.sleep(60)  # Make sure if we fetch the isuances that everything is up to date
        try:
            tft_tx_memo_hashes, tft_transactions_cursor = fetch_new_transaction_memo_hashes(
                wallet, tft_issuer, tft_transactions_cursor
            )
            tft_issuer_memo_hashes = [*tft_issuer_memo_hashes, *tft_tx_memo_hashes]

            for p in payments_to_process:
                if not already_issued_for_payment(p, tft_issuer_memo_hashes):
                    j.logger.info(f"Issuing {p.balance.balance} TFT to {p.from_address} for payment {p.transaction_hash}")
                    if preview:
                        continue
                    try:
                        wallet.transfer(
                        p.from_address,
                        amount=p.balance.balance,
                        asset=f"TFT:{tft_issuer}",
                        memo_hash=p.transaction_hash,
                        fund_transaction=False,
                        from_address=tft_issuer,
                        )
                    except NoTrustLine:
                       j.logger.error(f"{p.from_address} has no TFT trustline")
                    except TemporaryProblem as e:
                       j.logger.error(f"Temporaryproblem: {e}") 
                     
            payments_to_process, tfta_payments_cursor = fetch_new_payments_to_process(
                wallet,
                tfta_issuer,
                tfta_payments_cursor,
                f"TFTA:{tfta_issuer}",
                tft_issuer_memo_hashes,
            )
        except (jumpscale.core.exceptions.exceptions.Timeout,ConnectionError) :
            continue

if __name__ == "__main__":
    convert_tfta_to_tft()
