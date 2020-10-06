#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import stellar_sdk
import click
import requests
import decimal


def create_keypair():
    kp = stellar_sdk.Keypair.random()
    print("Key: {}".format(kp.secret))
    print("Address: {}".format(kp.public_key))
    return kp


@click.command()
def create_account():
    create_keypair()


if __name__ == "__main__":
    create_account()
