#!/usr/bin/env python
# pylint: disable=no-value-for-parameter
import click
import stellar_sdk
import datetime
import dateutil.parser

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

_HORIZON_NETWORKS = {
    "test": "https://horizon-testnet.stellar.org",
    "public": "https://horizon.stellar.org",
}


@click.command(help="Exports the tokenissuanes for TFT or TFTA")
@click.option("--network", type=click.Choice(["test", "public"], case_sensitive=False), default="public")
def export(network):

    issuances = []
    horizon_server = stellar_sdk.Server(_HORIZON_NETWORKS[network])
    for token in ("TFT", "TFTA"):
        issuer = _ASSET_ISUERS[network][token]
        endpoint = horizon_server.operations().for_account(issuer)
        endpoint.limit(100)
        old_cursor = "old"
        new_cursor = ""
        while new_cursor != old_cursor:
            old_cursor = new_cursor
            endpoint.cursor(new_cursor)
            response = endpoint.call()
            next_link = response["_links"]["next"]["href"]
            next_link_query = parse.urlsplit(next_link).query
            new_cursor = parse.parse_qs(next_link_query, keep_blank_values=True)["cursor"][0]
            for operation in response["_embedded"]["records"]:
                if ("asset_code" not in operation) or operation["asset_code"] != token:
                    continue
                amount = float(operation["amount"])
                if operation["to"] == issuer:
                    amount *= -1
                issued_at = dateutil.parser.parse(operation["created_at"])
                issuances.append({"token": token, "amount": amount, "issued_at": issued_at})

    def sort_key(a):
        return a["issued_at"]

    issuances.sort(key=sort_key)
    total_tft = 0.0
    total_tfta = 0.0
    for issuance in issuances:
        amount_tft = 0
        amount_tfta = 0
        if issuance["token"] == "TFT":
            amount_tft = issuance["amount"]
            total_tft += amount_tft
        else:
            amount_tfta = issuance["amount"]
            total_tfta += amount_tfta
        print(
            f"{issuance['issued_at']:%Y/%m/%d},{amount_tft},{amount_tfta},{total_tft},{total_tfta},{total_tft+total_tfta}"
        )


if __name__ == "__main__":
    export()
