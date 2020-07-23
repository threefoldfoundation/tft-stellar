#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

from jumpscale.loader import j
import click
import stellar_sdk

from urllib import parse



_ASSET_ISUERS = {
    "test": {
        "TFT": "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3",
        "TFTA": "GB55A4RR4G2MIORJTQA4L6FENZU7K4W7ATGY6YOT2CW47M5SZYGYKSCT",
    },
    "public": {
        "TFT": "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
        "TFTA": "GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2",
    },
}
_HORIZON_NETWORKS = {"test": "https://horizon-testnet.stellar.org", "public": "https://horizon.stellar.org"}
class StatisticsCollector(object):
    def __init__(self,network:str):
        self._network=network

    @property
    def _horizon_server(self):
        server_url = _HORIZON_NETWORKS[self._network]
        return stellar_sdk.Server(horizon_url=server_url)

    def get_accounts(self,tokencode:str, issuer:str):
        locked_accounts=[]
        horizon_server=self._horizon_server
        asset=stellar_sdk.Asset(tokencode,issuer)
        accounts_endpoint=horizon_server.accounts().for_asset(asset).limit(50)
        old_cursor = "old"
        new_cursor = ""
        while new_cursor != old_cursor:
            old_cursor = new_cursor
            accounts_endpoint.cursor(new_cursor)
            response = accounts_endpoint.call()
            next_link = response["_links"]["next"]["href"]
            next_link_query = parse.urlsplit(next_link).query
            new_cursor = parse.parse_qs(next_link_query)["cursor"][0]
            accounts = response["_embedded"]["records"]
            for account in accounts:
                account_id = account["account_id"]
                preauth_signers = [signer["key"] for signer in account["signers"] if signer["type"] == "preauth_tx"]
                tokenbalances=[float(b["balance"]) for b in account["balances"] if b["asset_type"]=="credit_alphanum4" and b["asset_code"]==tokencode and b["asset_issuer"]==issuer]
                tokenbalance=tokenbalances[0] if tokenbalances  else 0
                if len(preauth_signers)> 0:
                    locked_accounts.append({"account":account_id,"amount":tokenbalance, "preauth_signers":preauth_signers})
        return locked_accounts

    def getstatistics(self,tokencode:str):
        stats={"asset":tokencode}
        horizon_server=self._horizon_server
        asset_issuer=_ASSET_ISUERS[self._network][tokencode]
        stats["issuer"]=asset_issuer
        response=horizon_server.assets().for_code(tokencode).for_issuer(asset_issuer).call()
        record=response["_embedded"]["records"][0]
        stats["total"]=float(record["amount"])
        stats["num_accounts"]=record["num_accounts"]
        locked_accounts= self.get_accounts(tokencode,asset_issuer)
        total_locked =0.0
        for locked_account in locked_accounts:
            total_locked+=locked_account["amount"]
        stats["total_locked"]=total_locked
        return stats

@click.command(help="Convert burned TFTA's from the selling service to TFT's")
@click.argument("tokencode", type=click.Choice(['TFT','TFTA','FreeTFT']), default='TFT')
@click.option("--network", type=click.Choice(['test','public'],case_sensitive=False),default='public')
def show_stats(tokencode,network):
    print(f"Statistics for {tokencode} on the {network} network" )
    collector=StatisticsCollector(network)
    stats=collector.getstatistics(tokencode)
    print(f"Total amount of tokens: {stats['total']}")
    print(f"Number of accounts: {stats['num_accounts']}")
    print(f"Amount of locked tokens: {stats['total_locked']}")

if __name__ == "__main__":
    show_stats()