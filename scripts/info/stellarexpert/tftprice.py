#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
import requests
import datetime
import time


def xlm_price_at(xlm_usd_values, timestamp):
    i = 1
    while i < len(xlm_usd_values) - 1:
        if xlm_usd_values[i - 1][0] > timestamp and xlm_usd_values[i][0] < timestamp:
            return xlm_usd_values[i - 1][1]
        i += 1


# May 2021 timestamp: 1619827200
# June 21021 timestamp: 1622419200
@click.command(help="Calculate the tft price using stellar.expert")
@click.argument("starttimestamp", required=False, type=int, default=0)
@click.argument("endtimestamp", required=False, type=int, default=0)
def tft_price_command(starttimestamp, endtimestamp):
    if endtimestamp == 0:
        endtimestamp = int(time.time()) + 3600
    # Get xlm prices in USD
    r = requests.get("https://api.stellar.expert/explorer/public/xlm-price")
    r.raise_for_status()
    xlm_usd_values = r.json()  # it is returned in reverse tmiestamp order
    # Make sure all our values match
    first_value = xlm_usd_values[0]
    first_value[0] = int(time.time()) + 1
    xlm_usd_values[0] = first_value

    # Get TFT prices in XLM
    r = requests.get(
        "https://api.stellar.expert/explorer/public/asset/TFT-GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47/stats-history"
    )
    r.raise_for_status()
    history = r.json()

    relevant_history = [
        {"ts": i["ts"], "price": i["price"], "traded_amount": i["traded_amount"]} for i in history if "price" in i
    ]

    weighted_average_price = 0.0
    total_volume = 0.0
    for i in relevant_history:
        timestamp = i["ts"]
        if timestamp < starttimestamp or timestamp > endtimestamp:
            continue
        xlm_price = xlm_price_at(xlm_usd_values, timestamp)
        high = i["price"][1]
        usd_high = high * xlm_price
        low = i["price"][2]
        usd_low = low * xlm_price
        average = (usd_high + usd_low) / 2
        volume = i["traded_amount"] / 10000000
        weighted_average_price += average * volume
        total_volume += volume

        print(
            f"{datetime.datetime.fromtimestamp(timestamp)} high: {usd_high:.5f} USD low: {usd_low:.5f} USD volume: {volume}"
        )

    weighted_average_price = weighted_average_price / total_volume
    print(f"Weighted average price = { weighted_average_price:.5f}")


if __name__ == "__main__":
    tft_price_command()
