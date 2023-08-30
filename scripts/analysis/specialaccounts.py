#!/usr/bin/env python

# pylint: disable=no-value-for-parameter

import click
import sqlite3
import pandas

@click.command(help="Loads the list of special walletsin an sqlite database")
@click.argument("specialaccountsfile", default="specialaccounts.csv",type=click.Path())
@click.argument("dbfile", default="tft_data.db", type=click.Path())
def load_data( specialaccountsfile, dbfile):
    db_connection=sqlite3.connect(dbfile)
    # Load the special wallets
    data=pandas.read_csv(specialaccountsfile)
    print(data)
    # Write it to sqlite 
    data.to_sql("specialaccounts",db_connection,if_exists='replace',index=False)
 
    db_connection.commit()
    db_connection.close()

if __name__ == "__main__":
    load_data()