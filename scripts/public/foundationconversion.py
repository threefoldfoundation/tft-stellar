import time,math

from datetime import datetime
_TFT_FULL_ASSETCODE="TFT:GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47"
_TFTA_FULL_ASSETCODE="TFTA:GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2"
tfchain_address=''
stellar_address=''
converter_wallet = j.clients.stellar.converter
tfchain_client = j.clients.tfchain.get("tfchain")
# get balance from tfchain
unlockhash = tfchain_client.unlockhash_get(tfchain_address)
balance = unlockhash.balance()

memo_hash = None
sorted_transactions = sorted(unlockhash.transactions, key=lambda tx: tx.height, reverse=True)
for tx in sorted_transactions:
    if tx.version.value == 176:
        memo_hash = tx.id



unlocked_tokens = balance.available.value
locked_tokens = balance.locked.value

unconfirmed_unlocked_tokens = balance.unconfirmed.value
unconfirmed_locked_tokens = balance.unconfirmed_locked.value

if not unconfirmed_unlocked_tokens.is_zero():
    raise Exception("Can't migrate right now, address had unconfirmed unlocked balance.")

if not unconfirmed_locked_tokens.is_zero():
    raise Exception("Can't migrate right now, address had unconfirmed locked balance.")

if not unlocked_tokens.is_zero():
    issuer_address = _TFT_FULL_ASSETCODE.split(":")[1]
    converter_wallet.transfer(stellar_address,"{0:.7f}".format(unlocked_tokens),_TFT_FULL_ASSETCODE,memo_hash=memo_hash,fund_transaction=False,from_address=issuer_address)


if not locked_tokens.is_zero():
    for tx in unlockhash.transactions:
        for coin_output in tx.coin_outputs:
            lock_time = coin_output.condition.lock.value
            if lock_time == 0:
                break
            lock_time_date = datetime.fromtimestamp(lock_time)
            # if lock time year is before 2021 be convert to TFTA
            if lock_time_date.year < 2021:
                asset = _TFTA_FULL_ASSETCODE
            # else we convert to TFT
            else:
                asset = _TFT_FULL_ASSETCODE
            issuer_address = asset.split(":")[1]
            if time.time() < lock_time:
                converter_wallet.transfer(stellar_address,"{0:.7f}".format(coin_output.value.value),asset,math.ceil(lock_time),memo_hash=memo_hash,fund_transaction=False,from_address=issuer_address)
                        