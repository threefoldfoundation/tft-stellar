#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
import stellar_sdk
from stellar_sdk.exceptions import Ed25519SecretSeedInvalidError
from stellarconstants import PUBLIC_HORIZON_SERVER, DEFAULT_TRANSACTION_TIMEOUT


def set_home_domain(tokencode, home_domain, issuer_secret, network):
    try:
        issuer_keypair = stellar_sdk.Keypair.from_secret(issuer_secret)
    except Ed25519SecretSeedInvalidError:
        raise click.BadOptionUsage("--issuer_secret", "Invalid issuer secret")
    issuer_address = issuer_keypair.public_key

    horizon_server = stellar_sdk.Server() if network == "test" else stellar_sdk.Server(PUBLIC_HORIZON_SERVER)
    base_fee = horizon_server.fetch_base_fee()
    issuer_account = horizon_server.load_account(issuer_address)
    transaction = (
        stellar_sdk.transaction_builder.TransactionBuilder(
            issuer_account,
            network_passphrase=stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
            if network == "test"
            else stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
        .append_set_options_op(home_domain=home_domain)
        .build()
    )
    transaction.sign(issuer_keypair)
    horizon_server.submit_transaction(transaction)


@click.command(
    help="Set the homedomain on a custom asset as described at https://www.stellar.org/developers/guides/issuing-assets.html#discoverablity-and-meta-information "
)
@click.argument("tokencode", type=str, required=True)
@click.argument("home_domain", type=str, required=True)
@click.option("--network", type=click.Choice(["public", "test"], case_sensitive=False), default="public")
@click.option("--issuer_secret", type=str, required=True, help="The secret key of the issuer")
def set_home_domain_command(tokencode, home_domain, issuer_secret, network):
    set_home_domain(tokencode, home_domain, issuer_secret, network)


if __name__ == "__main__":
    set_home_domain_command()
