#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
import base64, binascii
from urllib import parse
import stellar_sdk
import sqlite3
import pandas
import decimal
from sqlalchemy import DECIMAL


ISSUERS = {
    "TFT": "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
    "TFTA": "GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2",
}


@click.command(help="Fetches all issued TFT and TFTA and puts this in an sqlite database")
@click.argument("dbfile", default="tft_data.db", type=click.Path())
def list_issued(dbfile):
    #issuance_data=pandas.DataFrame(columns=('transaction','token','amount','to','memo'))
    issuance_data = None 
    #tfta_destructions_data=pandas.DataFrame(columns=('transaction','amount'))
    tfta_destructions_data = None
    horizon_server = stellar_sdk.Server("https://horizon.stellar.org")
    tx_endpoint = horizon_server.transactions()
    tx_endpoint.limit = 50
    for tokencode, issuer in ISSUERS.items():
        tx_endpoint.for_account(issuer)
        tx_endpoint.include_failed(False)
        old_cursor = "old"
        new_cursor = ""
        while old_cursor != new_cursor:
            old_cursor = new_cursor
            tx_endpoint.cursor(new_cursor)
            response = tx_endpoint.call()
            next_link = response["_links"]["next"]["href"]
            next_link_query = parse.urlsplit(next_link).query
            new_cursor = parse.parse_qs(next_link_query)["cursor"][0]
            response_transactions = response["_embedded"]["records"]
            for response_transaction in response_transactions:
                try:
                    env = stellar_sdk.transaction_envelope.TransactionEnvelope.from_xdr(
                    response_transaction["envelope_xdr"], stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE
                    )
                except ValueError:
                   print(f"Unable to parse transaction {response_transaction['id']}")
                   continue 
                for operation in env.transaction.operations:
                    if  not isinstance(operation,stellar_sdk.Payment):
                        continue
                    if not (operation.asset.code==tokencode and operation.asset.issuer ==issuer):
                        continue
                    if (operation.source is None and env.transaction.source.account_id ==issuer) or (operation.source is not None and operation.source.account_id == issuer):
                        if response_transaction["memo_type"] != "hash":
                            print(f"{response_transaction['id']} has no memo")
                            continue
                        memo = binascii.hexlify(base64.b64decode(response_transaction["memo"])).decode("utf-8")
                        data={'transaction':response_transaction['id'],'token':tokencode,'amount':operation.amount, 'to':operation.destination.account_id,'memo':memo}
                        if issuance_data is None:
                            issuance_data=pandas.DataFrame(data,index=[0])
                        else:
                            issuance_data.loc[len(issuance_data)] = data
                        continue
                    else:
                        if operation.destination.account_id==issuer and tokencode=='TFTA':
                            data={'transaction':response_transaction['id'],'amount':operation.amount}
                            if tfta_destructions_data is None:
                                tfta_destructions_data=pandas.DataFrame(data ,index=[0])
                            else: 
                                tfta_destructions_data.loc[len(tfta_destructions_data)]=data
                      

    

    db_connection=sqlite3.connect(dbfile)
    issuance_data.to_sql("minted",db_connection,if_exists='replace',index=False)
    db_connection.commit()
    tfta_destructions_data.to_sql('tftadestruction',db_connection,if_exists='replace',index=False)
    db_connection.close()

if __name__ == "__main__":
    list_issued()
