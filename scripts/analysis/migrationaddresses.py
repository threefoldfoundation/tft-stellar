#!/usr/bin/env python

# pylint: disable=no-value-for-parameter

import click
import pandas
import sqlalchemy
import os,sys


CURRENT_FULL_PATH = os.path.dirname(os.path.abspath(__file__))
lib_path = CURRENT_FULL_PATH + "/../../lib/"
sys.path.append(lib_path)

def stellar_address_to_tfchain_address(stellar_address):
    from tfchaintypes.CryptoTypes import PublicKey, PublicKeySpecifier
    from stellar_sdk import strkey

    raw_public_key = strkey.StrKey.decode_ed25519_public_key(stellar_address)
    rivine_public_key = PublicKey(PublicKeySpecifier.ED25519, raw_public_key)
    return str(rivine_public_key.unlockhash)

@click.command(help="Finds the stellar addresses for migrated Rivine addresses and stores it in an sqlite database")
@click.argument("dbfile", default="tft_data.db", type=click.Path())
@click.argument("matchfile", default="../conversion/matched.txt",type=click.Path())
def find_stellar_adresses( dbfile,matchfile):
    # Multisig addresses were not supported and someone lost it's Rivine secret
    migrated_addresses=pandas.read_table(matchfile,sep=' ',names=('rivineaddress','stellaraddress'))
    db_engine=sqlalchemy.create_engine(f"sqlite:///{dbfile}")
    rivine_data=pandas.read_sql_table("rivine",db_engine)
    # Drop stellaraddress column if it already exists
    rivine_data=rivine_data.filter(['rivineaddress','locktransaction','free','locked','total'], axis=1)
    #print(rivine_data)
    minted_data=pandas.read_sql_table("minted",db_engine)
    #print(minted_data)
    pandas.set_option('display.max_colwidth',1000)
    for _, rivine_row in rivine_data.iterrows():
        rivine_address=rivine_row["rivineaddress"]
        #Check if there already is a match ( from the matchfile)
        already_matched=migrated_addresses.loc[migrated_addresses['rivineaddress']==rivine_address]
        if not already_matched.empty:
            continue
        
        single_rivine_address_mints=minted_data.loc[minted_data['memo']==rivine_row["locktransaction"]]
        #print(single_rivine_address_mints)
        if single_rivine_address_mints.empty:
            continue
        
        stellar_address=None
        for _, mintrow in single_rivine_address_mints.iterrows():
            # blockcreators were converted to GDW4LVQ6DYDUBQWKK25CYIEWTZRWLCD24WBHHDZEPS426KL4II34EAO4
            if stellar_address_to_tfchain_address(mintrow["to"]) == rivine_address or mintrow["to"] =="GDW4LVQ6DYDUBQWKK25CYIEWTZRWLCD24WBHHDZEPS426KL4II34EAO4":
                stellar_address= mintrow["to"] 
                #print(f'rivine address {rivine_row["rivineaddress"]} corresponds to Stellar address {stellar_address}')
                data= {'rivineaddress':rivine_address,'stellaraddress':stellar_address}
                
                migrated_addresses.loc[len(migrated_addresses)] = data
                break
        if stellar_address is None:
            print(f'Should figure out  {rivine_row["rivineaddress"]}')
            print(single_rivine_address_mints)


    combined_data=rivine_data.merge(migrated_addresses,how='left',on='rivineaddress')

    combined_data.to_sql("rivine",db_engine,if_exists='replace',index=False)



if __name__ == "__main__":
    find_stellar_adresses()