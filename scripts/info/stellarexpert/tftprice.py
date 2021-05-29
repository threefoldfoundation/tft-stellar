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


@click.command(help="Calculate the tft price using stellar.expert")
@click.argument("starttimestamp", required=False, type=int, default=0)
def tft_price_command(starttimestamp):
    # Get xlm prices in USD
    r = requests.get("https://api.stellar.expert/explorer/public/xlm-price")
    r.raise_for_status()
    xlm_usd_values = r.json()  # it is returned in reverse tmiestamp order
    # Make sure all our values match
    first_value = xlm_usd_values[0]
    first_value[0] = int(time.time()) + 1
    xlm_usd_values[0] = first_value

    # Get TFT bprices in XLM
    r = requests.get(
        "https://api.stellar.expert/explorer/public/asset/TFT-GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47"
    )
    r.raise_for_status()
    parsed_response = r.json()
    if not "history" in parsed_response:
        print("No history in stellar.expert response")
        print(parsed_response)
        return

    history = parsed_response["history"]
    relevant_history = [
        {"ts": i["ts"], "price": i["price"], "traded_amount": i["traded_amount"]} for i in history if "price" in i
    ]
    weighted_average_price = 0.0
    total_volume = 0.0
    for i in relevant_history:
        timestamp = i["ts"]
        if timestamp < starttimestamp:
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

        print(f"{datetime.datetime.fromtimestamp(timestamp)}: high: {usd_high} USD low: {usd_low} USD volume: {volume}")
    weighted_average_price = weighted_average_price / total_volume
    print("Weighted average price=", weighted_average_price)


if __name__ == "__main__":
    tft_price_command()
