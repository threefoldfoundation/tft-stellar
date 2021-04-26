#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import stellar_sdk
from stellar_sdk.transaction_builder import Keypair
import click

_HORIZON_NETWORKS = {"test": "https://horizon-testnet.stellar.org", "public": "https://horizon.stellar.org"}

ASSET_ISSUERS = {
    "test": {
        "TFT": "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3",
        "BTC": "GBMDRYGRFNPCGNRYVTHOPFE7F7L566ZLZM7XFQ2UWWIE3NVSO7FA5MFY",
    },
    "public": {
        "TFT": "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
        "BTC": "GCNSGHUCG5VMGLT5RIYYZSO7VQULQKAJ62QA33DBC5PPBSO57LFWVV6P",
    },
}


def create_buy_order(buying_account_secret, amount, network):
    buying_asset_code = "TFT"
    buying_asset_issuer = ASSET_ISSUERS[network][buying_asset_code]
    selling_asset_code = "BTC"
    selling_asset_issuer = ASSET_ISSUERS[network][selling_asset_code]
    price = "0.0000019"

    buying_kp = Keypair.from_secret(buying_account_secret)

    horizon_server = stellar_sdk.Server(_HORIZON_NETWORKS[network])
    source_account = horizon_server.load_account(buying_kp.public_key)
    transaction = (
        stellar_sdk.TransactionBuilder(
            source_account=source_account,
            network_passphrase=stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
            if network == "test"
            else stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE,
            base_fee=0,
        )
        .append_manage_buy_offer_op(
            selling_code=selling_asset_code,
            selling_issuer=selling_asset_issuer,
            buying_code=buying_asset_code,
            buying_issuer=buying_asset_issuer,
            amount=amount,
            price=price,
        )
        .set_timeout(60)
        .build()
    )
    transaction.sign(buying_kp)
    return transaction


def fee_bump(funding_account_secret, buy_transaction: stellar_sdk.TransactionEnvelope, network):
    funding_kp = Keypair.from_secret(funding_account_secret)

    horizon_server = stellar_sdk.Server(_HORIZON_NETWORKS[network])
    base_fee = horizon_server.fetch_base_fee()
    fb_txe = stellar_sdk.TransactionBuilder.build_fee_bump_transaction(
        fee_source=funding_kp.public_key,
        base_fee=base_fee,
        inner_transaction_envelope=buy_transaction,
        network_passphrase=stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
        if network == "test"
        else stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE,
    )
    fb_txe.sign(funding_kp)
    response = horizon_server.submit_transaction(fb_txe)
    print(f"Submittted fee bumped transaction {response['hash']}")


@click.command()
@click.argument("buying_account_secret", type=str)
@click.argument("funding_account_secret", type=str)
@click.argument("amount", type=str)
@click.option("--network", type=click.Choice(["test", "public"], case_sensitive=False), default="test")
def fund_buy_order(buying_account_secret, funding_account_secret, amount, network):
    network = "test"
    buy_tx = create_buy_order(buying_account_secret, amount, network)
    fee_bump(funding_account_secret, buy_tx, network)


if __name__ == "__main__":
    fund_buy_order()
