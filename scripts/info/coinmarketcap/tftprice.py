#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
import requests
import datetime
import time



# May 2021 timestamp: 1619827200
# June 21021 timestamp: 1622419200
@click.command(help="Calculate the tft price using coinmarketcap")
@click.argument("starttimestamp", required=False, type=int, default=0)
@click.argument("endtimestamp", required=False, type=int, default=0)
def tft_price_command(starttimestamp, endtimestamp):
    if endtimestamp == 0:
        endtimestamp = int(time.time()) + 3600

    # Get TFT bprices in XLM
    r = requests.get(
        "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id=6500&range=3M&convertIds=1084 "   
    )
    r.raise_for_status()
    history = r.json()["data"]["points"]


    weighted_average_price = 0.0
    total_volume = 0.0
    for ts,data in history.items():
        timestamp=int(ts)
        if timestamp < starttimestamp or timestamp > endtimestamp:
            continue
        price=data["v"][0]
        volume=data["v"][1]
        weighted_average_price += price * volume
        total_volume += volume

        print(
            f"{datetime.datetime.fromtimestamp(timestamp)} price: {price:.5f} USD volume: {volume} USD"
        )

    weighted_average_price = weighted_average_price / total_volume
    print(f"Weighted average price = { weighted_average_price:.5f}")


if __name__ == "__main__":
    tft_price_command()
