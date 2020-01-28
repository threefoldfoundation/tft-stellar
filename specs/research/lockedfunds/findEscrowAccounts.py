#!/usr/bin/env python
# pylint: disable=no-value-for-parameter


import click
import stellar_sdk
import decimal
from urllib import parse
import sys
sys.path.append('..')
from common.assets import asset_from_full_string

@click.command()
@click.argument('receiver', type=str)
@click.option('--asset',type=str,default='TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3')
def find_escrow_accounts(receiver, asset):
    stellar_asset= asset_from_full_string(asset)
    horizon_server = stellar_sdk.Server()
    accounts_endpoint= horizon_server.accounts()
    accounts_endpoint.signer(receiver)
    old_cursor='old'
    new_cursor=''
    while new_cursor!= old_cursor:
        old_cursor= new_cursor
        accounts_endpoint.cursor(new_cursor)
        response= accounts_endpoint.call()
        next_link= response['_links']['next']['href']
        next_link_query = parse.urlsplit(next_link).query
        new_cursor= parse.parse_qs(next_link_query)['cursor'][0]
        accounts= response['_embedded']['records']
        for account in accounts:
            account_id=account['account_id']
            if account_id== receiver: continue # Do not take the receiver's account 
            balances=account['balances']
            asset_balances = [balance for balance in balances if balance['asset_type']==stellar_asset.guess_asset_type() and balance['asset_code']== stellar_asset.code and balance['asset_issuer']==stellar_asset.issuer]
            asset_balance= decimal.Decimal(0)
            for balance in asset_balances:
                asset_balance+= decimal.Decimal(balance['balance'])
            if asset_balance== decimal.Decimal(): continue # 0 so skip
            
            all_signers= account['signers']
            preauth_signers= [signer['key'] for signer in all_signers if signer['type']=='preauth_tx']
            #TODO check the tresholds and signers
            #TODO if we can merge, the amount is unlocked ( if len(preauth_signers))==0
            print('Account {account} with {asset_balance} {asset_code} has unlocktransaction hashes {unlockhashes}'.format(account=account_id,asset_balance=asset_balance, asset_code=stellar_asset.code, unlockhashes=preauth_signers))

if __name__ == '__main__':
  find_escrow_accounts()