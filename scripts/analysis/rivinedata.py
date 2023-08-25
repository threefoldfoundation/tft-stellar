#!/usr/bin/env python

# pylint: disable=no-value-for-parameter

import click
import sqlite3
import pandas

@click.command(help="Loads rivine TFT data in an sqlite database")
@click.argument("deauthorizationsfile", default="../conversion/deauthorizations.txt",type=click.Path())
@click.argument("balancesfile", default="../conversion/deauthorizedbalances.txt",type=click.Path())
@click.argument("dbfile", default="tft_data.db", type=click.Path())
def load_rivine_data( deauthorizationsfile,balancesfile, dbfile):
    db_connection=sqlite3.connect(dbfile)
    # Load the deauthorization transactions
    locking_data=pandas.read_table(deauthorizationsfile,sep=' ',names=('locktransaction','rivineaddress'))
    # Re-order columns
    locking_data=locking_data[['rivineaddress','locktransaction']]

    # Load the rivine balances
    balances_data=pandas.read_table(balancesfile,sep=' ',header=0)
    # Join the data
    combined_data=pandas.merge(locking_data,balances_data,how="inner",on="rivineaddress") 
    
    # Write it to sqlite 
    combined_data.to_sql("rivine",db_connection,if_exists='replace',index=False)
 
    db_connection.commit()
    db_connection.close()

if __name__ == "__main__":
    load_rivine_data()