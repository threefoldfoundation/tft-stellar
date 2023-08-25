#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
import requests
import json
import base64, binascii
import time
from urllib import parse
import stellar_sdk


ISSUERS = {
    "TFT": "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
    "TFTA": "GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2",
}


@click.command(help="List issued TFT and TFTA")
def list_issued():
    horizon_server = stellar_sdk.Server("https://horizon.stellar.org")
    tx_endpoint = horizon_server.transactions()
    tx_endpoint.limit = 50
    for tokencode, issuer in ISSUERS.items():
        tx_endpoint.for_account(issuer)
        tx_endpoint.include_failed(False)
        old_cursor = "old"
        new_cursor = ""
        while old_cursor != new_cursor:
            old_cursor = new_cursor
            tx_endpoint.cursor(new_cursor)
            response = tx_endpoint.call()
            next_link = response["_links"]["next"]["href"]
            next_link_query = parse.urlsplit(next_link).query
            new_cursor = parse.parse_qs(next_link_query)["cursor"][0]
            response_transactions = response["_embedded"]["records"]
            for response_transaction in response_transactions:
                if response_transaction["memo_type"] != "hash":
                    continue
                memo = binascii.hexlify(base64.b64decode(response_transaction["memo"])).decode("utf-8")
                
                env = stellar_sdk.transaction_envelope.TransactionEnvelope.from_xdr(
                    response_transaction["envelope_xdr"], stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE
                )
                paymentoperation = env.transaction.operations[0]

                print(
                    f"{memo} {paymentoperation.amount} {tokencode} {paymentoperation.destination.account_id} {response_transaction['id']}"
                )


if __name__ == "__main__":
    list_issued()
