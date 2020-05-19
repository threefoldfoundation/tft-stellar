#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
import os
import toml
from brandedtoken import create_branded_token


BRANDEDTOKEN_CONFIGDIRS = "../config/brandedtokens"

@click.command(help="Rename Threefold project branded tokens")
def rename_branded_tokens_command():
     for tokencode in os.listdir(BRANDEDTOKEN_CONFIGDIRS):
         for network in ('public','testnet'):
            stellartomfile=os.path.join(BRANDEDTOKEN_CONFIGDIRS, tokencode,network, "stellar.toml")
            brandedtokenconfig = toml.load(stellartomfile)
            brandedtokenconfig['CURRENCIES'][0]['code']=tokencode
            with open(stellartomfile, "w") as configfile:
                toml.dump(brandedtokenconfig, configfile)
            globalconfigfilename = os.path.join("../config",network, "stellar.toml")
            globalconfig = toml.load(globalconfigfilename)
            globalconfig["CURRENCIES"].append(brandedtokenconfig['CURRENCIES'][0])
            with open(globalconfigfilename, "w") as configfile:
                toml.dump(globalconfig, configfile)

if __name__ == "__main__":
    rename_branded_tokens_command()

