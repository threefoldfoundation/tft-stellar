#!/usr/bin/env python3
# pylint: disable=no-value-for-parameter
import click
from jumpscale.loader import j
import stellar_sdk
import os
from  jumpscale.clients.stellar.exceptions import UnAuthorized



ISSUERS = {
    "public": {
        "TFT": "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
        "TFTA": "GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2",
    },
    "testnet": {
        "TFT": "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3",
        "TFTA": "GB55A4RR4G2MIORJTQA4L6FENZU7K4W7ATGY6YOT2CW47M5SZYGYKSCT",
    },
}


def do_basic_validation(tx_envelope:stellar_sdk.TransactionEnvelope):
    assert type(tx_envelope.transaction.memo)==stellar_sdk.HashMemo
    assert len(tx_envelope.transaction.operations)==1
    assert type(tx_envelope.transaction.operations[0])==stellar_sdk.operation.Payment

def print_transaction_data(tx_envelope:stellar_sdk.TransactionEnvelope, status:str="Sending"):
    memo_hash= tx_envelope.transaction.memo.memo_hash
    sequence=tx_envelope.transaction.sequence
    paymentoperation=tx_envelope.transaction.operations[0]
    asset=paymentoperation.asset
    amount=paymentoperation.amount
    destination=paymentoperation.destination
    tx_envelope.signatures
    print(f"{status} {amount} {asset.code}:{asset.issuer} to {destination} with memo {memo_hash.hex()} and sequence number {sequence}")

@click.command(help="Minting transactions signer")
@click.argument("inputfile", default="payouts_to_sign.txt", type=click.File("r"))
@click.argument("outputfile", default="payouts_signed.txt",type=click.File("w"))
@click.option("--preview/--no-preview",default=False)
@click.option("--walletname",type=str,default="TFCosigningwallet")
def sign_payments_command(inputfile,outputfile, preview,walletname):
    wallet=j.clients.stellar.find(walletname)
    if wallet is None:
        raise click.BadParameter(f"Wallet with name {walletname} does not exist")
    network_passphrase=stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE if wallet.network.value=="STD" else stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
    outputstrings=[]
    for input_xdr in inputfile.readlines():
        tx_envelope=stellar_sdk.TransactionEnvelope.from_xdr(input_xdr,network_passphrase)
        do_basic_validation(tx_envelope)
        if preview:
            print_transaction_data(tx_envelope)
            continue
        try:
            print_transaction_data(tx_envelope,"Signing")
            wallet.sign(input_xdr)
            print_transaction_data(tx_envelope,"Sent")
        except UnAuthorized as e:
            outputstrings.append(f"{e.transaction_xdr}")
        except stellar_sdk.exceptions.BadRequestError as e:
            if e.status == 400:
                resultcodes = e.extras["result_codes"]
                if resultcodes["transaction"] == "tx_bad_seq":
                    outputstrings.append(f"{e.extras['envelope_xdr']}") 
                    continue
            raise e
    outputfile.write("\n".join(outputstrings))    
    
        
if __name__ == "__main__":
    sign_payments_command()