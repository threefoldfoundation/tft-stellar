#!/usr/bin/env python
# pylint: disable=no-value-for-parameter
import click
import stellar_sdk
import datetime
import os
import sys
import time

from urllib import parse


current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../lib/stats/")
from stats import get_locked_accounts, get_unlockhash_transaction, _NETWORK_PASSPHRASES


def lookup_lock_time(network, preauth_signer: str):
    unlock_tx = get_unlockhash_transaction(network, unlockhash=preauth_signer)
    if unlock_tx is None:
        return None
    txe = stellar_sdk.TransactionEnvelope.from_xdr(unlock_tx["transaction_xdr"], _NETWORK_PASSPHRASES[network])
    tx = txe.transaction
    if tx.preconditions is not None and tx.preconditions.time_bounds is not None:
        return tx.preconditions.time_bounds.min_time
    return None

@click.command(help="Lists information about timelocked TFT (owner account, TFT, escrow account unlocktime, status)")
@click.option("--network", type=click.Choice(["test", "public"], case_sensitive=False), default="public")
def list_lockedTFT_info(network):

    locked_accounts, _ , _ = get_locked_accounts(network, "TFT",[])
    now = time.time()
    for escrow_account in locked_accounts:
        for signer in escrow_account["signers"]:
            if signer["type"]=="ed25519_public_key" and signer["key"]!=escrow_account['account']:
                owner_account=signer["key"]
        unlock_time = lookup_lock_time(network,escrow_account["preauth_signers"][0])
        print(
            f"{owner_account},{escrow_account['amount']},{escrow_account['account']} {unlock_time} {'Free' if unlock_time < now else 'Locked'}"
        )


if __name__ == "__main__":
    list_lockedTFT_info()
