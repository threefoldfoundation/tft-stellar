#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
import os
from brandedtoken import create_branded_token


BRANDEDTOKEN_CONFIGDIRS = "../config/brandedtokens"

@click.command(help="Create production Threefold project branded tokens")
@click.option("--activator_secret", type=str, required=True, help="The secret key of the activating account")
def create_prod_branded_tokens_command(activator_secret):
     for tokencode in os.listdir(BRANDEDTOKEN_CONFIGDIRS):
        create_branded_token(tokencode,None,activator_secret,'public')


if __name__ == "__main__":
    create_prod_branded_tokens_command()
