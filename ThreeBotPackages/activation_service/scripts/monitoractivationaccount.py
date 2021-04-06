#!/usr/bin/env python
# pylint: disable=no-value-for-parameter
import click
import stellar_sdk



@click.command(help="Verification of the vesting service")
@click.option("--activationaccount", type=str,default="GCKLGWHEYT2V63HC2VDJRDWEY3G54YSHHPOA6Q3HAPQUGA5OZDWZL7KW")
@click.option("--network", type=click.Choice(["test", "public"], case_sensitive=False), default="public")
def monitor(activationaccount,network):
    horizon_server=stellar_sdk.Server("https://horizon-testnet.stellar.org" if network=="test" else "https://horizon.stellar.org")
    accounts_endpoint=horizon_server.accounts().account_id(activationaccount)
   
    response = accounts_endpoint.call()
    xlm_balance=[float(balance["balance"]) for balance in response["balances"] if balance["asset_type"]=="native"][0]

    sponsored_balance=response["num_sponsoring"]* 0.5
    print(f"{activationaccount} holds {xlm_balance} XLM of which {xlm_balance-sponsored_balance} is free")
    
if __name__ == "__main__":
    monitor()
