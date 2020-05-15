#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import click
import stellar_sdk
from stellar_sdk.exceptions import Ed25519SecretSeedInvalidError
import os
import toml
from publishdomain import set_home_domain
from stellarconstants import PUBLIC_HORIZON_SERVER, DEFAULT_TRANSACTION_TIMEOUT

DEFAULT_HOME_DOMAINS = {"test": "www2.threefold.io", "public": "threefold.io"}

BRANDEDTOKEN_CONFIGDIRS = "../config/brandedtokens"
TFT_ISSUERS = {
    "test": "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3",
    "public": "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
}


def add_tft_trustline(source_kp, network):
    horizon_server = stellar_sdk.Server() if network == "test" else stellar_sdk.Server(PUBLIC_HORIZON_SERVER)
    base_fee = horizon_server.fetch_base_fee()
    source_account = horizon_server.load_account(source_kp.public_key)
    transaction = (
        stellar_sdk.transaction_builder.TransactionBuilder(
            source_account,
            network_passphrase=stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
            if network == "test"
            else stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
        .append_change_trust_op("TFT", TFT_ISSUERS[network])
        .build()
    )
    transaction.sign(source_kp)
    horizon_server.submit_transaction(transaction)


def activate_account(address, activator_secret, network):
    activator_keypair = stellar_sdk.Keypair.from_secret(activator_secret)
    horizon_server = stellar_sdk.Server() if network == "test" else stellar_sdk.Server(PUBLIC_HORIZON_SERVER)
    base_fee = horizon_server.fetch_base_fee()
    activator_account = horizon_server.load_account(activator_keypair.public_key)
    transaction = (
        stellar_sdk.transaction_builder.TransactionBuilder(
            activator_account,
            network_passphrase=stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
            if network == "test"
            else stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
        .append_create_account_op(address, "10")
        .build()
    )
    transaction.sign(activator_keypair)
    horizon_server.submit_transaction(transaction)


def create_keypair(tokencode):
    kp = stellar_sdk.Keypair.random()
    print(f"{tokencode} issuer secret key: {kp.secret}")
    print(f"{tokencode} issuer Address: {kp.public_key}")
    return kp


def update_stellar_configs(brandedtokenconfig: dict, tokencode, network, home_domain):
    # Create an individual stellar.toml config
    stellartoml = {}
    stellartoml["CURRENCIES"] = [brandedtokenconfig]
    configdir = os.path.join(BRANDEDTOKEN_CONFIGDIRS, tokencode, "testnet" if network == "test" else "public")
    if not os.path.exists(configdir):
        os.makedirs(configdir)
    with open(os.path.join(configdir, "stellar.toml"), "w") as configfile:
        toml.dump(stellartoml, configfile)

    # Update the global threefold stellar.toml
    if home_domain != DEFAULT_HOME_DOMAINS[network]:
        return
    globalconfigfilename = os.path.join("../config", "testnet" if network == "test" else "public", "stellar.toml")
    globalconfig = toml.load(globalconfigfilename)
    existingindex = -1
    for i in range(len(globalconfig["CURRENCIES"])):
        if globalconfig["CURRENCIES"][i]["code"] == tokencode:
            existingindex = i
            break
    if existingindex > -1:
        globalconfig["CURRENCIES"][existingindex] = brandedtokenconfig
    else:
        globalconfig["CURRENCIES"].append(brandedtokenconfig)
    with open(globalconfigfilename, "w") as configfile:
        toml.dump(globalconfig, configfile)


@click.command(help="Create a Threefold project branded token")
@click.argument("tokencode", type=str, required=True)
@click.option("--home_domain", type=str, required=False)
@click.option("--network", type=click.Choice(["public", "test"], case_sensitive=False), default="test")
@click.option("--activator_secret", type=str, required=True, help="The secret key of the activating account")
def create_branded_token(tokencode, home_domain, activator_secret, network):
    if not home_domain:
        home_domain = DEFAULT_HOME_DOMAINS[network]

    issuer_kp = create_keypair(tokencode)
    try:
        activate_account(issuer_kp.public_key, activator_secret, network)
    except Ed25519SecretSeedInvalidError:
        raise click.BadOptionUsage("--activator_secret", "Invalid activator secret")
    add_tft_trustline(issuer_kp, network)
    set_home_domain(tokencode, home_domain, issuer_kp.secret, network)

    brandedtokentemplateconfig = toml.load(os.path.join(BRANDEDTOKEN_CONFIGDIRS, tokencode, "templatestellar.toml"))

    brandedtokenconfig = {}
    brandedtokenconfig["code"] = tokencode
    brandedtokenconfig["issuer"] = issuer_kp.public_key
    brandedtokenconfig["display_decimals"] = 2
    brandedtokenconfig.update(brandedtokentemplateconfig)

    update_stellar_configs(brandedtokenconfig, tokencode, network, home_domain)


if __name__ == "__main__":
    create_branded_token()
