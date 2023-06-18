#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
import stellar_sdk
from decimal import Decimal


INITIAL_PRICES = {"XLM/TFT": Decimal("1"), "XLM/USDC": Decimal("10"), "TFT/USDC": Decimal("10")}
INITIAL_AMOUNTS = {"XLM/TFT": ("4500", "4500"), "XLM/USDC": ("4500", "450"), "TFT/USDC": ("500000", "50000")}

SUPPORTED_ASSETS = {
    "TFT": stellar_sdk.Asset("TFT", "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3"),
    "USDC": stellar_sdk.Asset("USDC", "GAHHZJT5OIK6HXDXLCSRDTTNPE52CMXFWW6YQXCBMHW2HUI6D365HPOO"),
    "XLM": stellar_sdk.Asset.native(),
}


def get_ordered_assets(asset_pair: str) -> list[stellar_sdk.Asset]:
    split_asset_pair = asset_pair.split("/")
    a = SUPPORTED_ASSETS[split_asset_pair[0]]
    b = SUPPORTED_ASSETS[split_asset_pair[1]]
    return [a, b] if stellar_sdk.LiquidityPoolAsset.is_valid_lexicographic_order(a, b) else [b, a]


@click.command(help="Manage testnet liquidity pools")
@click.argument("asset_pair", type=click.Choice(["XLM/TFT", "XLM/USDC", "TFT/USDC"]), required=True)
@click.argument("account_secret", type=str, required=True)
def manage_liquidity_pool_command(asset_pair, account_secret):
    manage_liquidity_pool(asset_pair,account_secret)


def manage_liquidity_pool(asset_pair, account_secret):
    try:
        account_keypair = stellar_sdk.Keypair.from_secret(account_secret)
    except stellar_sdk.exceptions.Ed25519SecretSeedInvalidError:
        raise click.BadArgumentUsage("Invalid account secret")

    account_address = account_keypair.public_key

    horizon_server = stellar_sdk.Server()

    try:
        account = horizon_server.load_account(account_address)
    except stellar_sdk.exceptions.NotFoundError:
        raise click.BadArgumentUsage("account does not exist")

    assets = get_ordered_assets(asset_pair)
    pool_asset = stellar_sdk.LiquidityPoolAsset(asset_a=assets[0], asset_b=assets[1])
    print("Adding liquidity for", pool_asset.asset_a.code, "/", pool_asset.asset_b.code)
    # check if the account already has a trustline to the iquidity pool
    has_trustline = False
    for balance in account.raw_data["balances"]:
        if (
            balance["asset_type"] == "liquidity_pool_shares"
            and balance["liquidity_pool_id"] == pool_asset.liquidity_pool_id
        ):
            has_trustline = True
            break
    # create the liquidity pool trustline if needed
    if not has_trustline:
        tx = stellar_sdk.TransactionBuilder(source_account=account).append_change_trust_op(asset=pool_asset).build()
        tx.sign(account_keypair)
        horizon_server.submit_transaction(tx)

    lp_response = horizon_server.liquidity_pools().for_reserves(assets).call()
    # by creating the trustline, we created the liquidity pool
    lp = lp_response["_embedded"]["records"][0]

    if Decimal(lp["total_shares"]).is_zero():
        print("No liquidity provided for pool", pool_asset.liquidity_pool_id, "yet")
        # Add liquidity
        exact_price = INITIAL_PRICES[asset_pair]
        min_price = exact_price - exact_price * Decimal("0.1")
        max_price = exact_price + exact_price * Decimal("0.1")
        max_amount_a, max_amount_b = INITIAL_AMOUNTS[asset_pair]
        tx = (
            stellar_sdk.TransactionBuilder(account)
            .append_liquidity_pool_deposit_op(
                pool_asset.liquidity_pool_id, max_amount_a, max_amount_b, min_price=min_price, max_price=max_price
            )
            .build()
        )
        tx.sign(account_keypair)
        horizon_server.submit_transaction(tx)
    else:
        print("Liquidity pool already has liquidity, add more or swap?")


if __name__ == "__main__":
    manage_liquidity_pool_command()
