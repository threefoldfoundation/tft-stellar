#!/usr/bin/env python

# pylint: disable=no-value-for-parameter

import click
import requests
import sqlite3
import os,sys
import time
import decimal


CURRENT_FULL_PATH = os.path.dirname(os.path.abspath(__file__))
lib_path = CURRENT_FULL_PATH + "/../../../lib/"
sys.path.append(lib_path)
from tfchainexplorer import TFCHAIN_EXPLORER,transaction_from_explorer_transaction
import tfchaintypes
from tfchaintypes.PrimitiveTypes import Currency

LAST_BLOCK=707919
class inputoutput:
    def __init__(self, address:str,value:decimal.Decimal):
        self.address=address
        self.value=value

def get_sender(senders:[], value)-> str:
    for sender in senders:
        if sender.value>= value:
            sender.value -= value
            return sender.address
    raise Exception("not enough value input")

TABLE_CREATION_SQL='CREATE TABLE IF NOT EXISTS rivinetxs ("transaction" TEXT, "from" TEXT, "to" TEXT, "amount" TEXT, "timestamp" INTEGER, "type" TEXT);'
INSERT_SQL='INSERT INTO rivinetxs("transaction","from","to","amount","timestamp","type") VALUES(?,?,?,?,?,?);'
@click.command(help="Fetches all Rivine transactions and stores them in an sqlite database")
@click.argument("dbfile", default="tft_data.db", type=click.Path())
@click.option('--start','-s',default=0, type=int)
@click.option('--preview/--no-preview', default=False)
def find_rivine_transactions( dbfile,start,preview):
    db_connection=sqlite3.connect(dbfile)
    db_connection.execute(TABLE_CREATION_SQL)
    block_height=start
    while block_height < LAST_BLOCK:
        print(f"Block {block_height}")
        response = requests.get(f"{TFCHAIN_EXPLORER}/explorer/blocks/{block_height}")
        response.raise_for_status
        block = response.json()["block"]
        for raw_transaction in block["transactions"]:
            timestamp=raw_transaction["timestamp"] 
            senders=[]
            cios=raw_transaction["coininputoutputs"]
            if cios is not None:
                for cio in cios:
                    senders.append(inputoutput(cio["unlockhash"],decimal.Decimal(cio["value"])))
                    
            transaction=transaction_from_explorer_transaction(raw_transaction)
            for output in transaction.coin_outputs:
                beneficiary=None
                if isinstance(output.condition,tfchaintypes.ConditionTypes.ConditionUnlockHash):
                    beneficiary=str(output.condition.unlockhash)
                elif isinstance(output.condition,tfchaintypes.ConditionTypes.ConditionLockTime):
                    beneficiary=str(output.condition.unlockhash)
                else:    
                    print(f"ROB: unparsed conditiontype in transaction {transaction.id}: {output.condition}")
                    return
                sender=get_sender(senders,output.value.value)
                if preview:
                    print(f"transaction {transaction.id} {output.value} from {sender} to {beneficiary} at {timestamp}, type: payment")
                else:
                    db_connection.execute(INSERT_SQL,(transaction.id,sender,beneficiary,str(output.value),timestamp,'payment'))
            for txfee in transaction.miner_fees:
                amount=txfee.value
                sender=get_sender(senders,amount)
                if preview:
                    print(f"transaction {transaction.id} {amount.copy_negate()} from {sender} at {timestamp} type: txfee")
                else:
                    db_connection.execute(INSERT_SQL,(transaction.id,sender,None,str(amount.copy_negate()),timestamp,'txfee'))
            for minerpayout in raw_transaction["minerpayouts"]:
                beneficiary=minerpayout["rawminerpayout"]["unlockhash"]
                amount=Currency.from_json(minerpayout["rawminerpayout"]["value"]).value
                if preview:
                    print(f"transaction {transaction.id} {amount} to {beneficiary} at {timestamp}, type: minerfee")
                else:
                    db_connection.execute(INSERT_SQL,(transaction.id,None,beneficiary,str(amount),timestamp,'minerfee'))
        db_connection.commit()
        time.sleep(0.5)  # give the explorer a break
        block_height+=1
    db_connection.close()
 

if __name__ == "__main__":
    find_rivine_transactions()