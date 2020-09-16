import base64
import json
from urllib.request import urlopen


from beaker.middleware import SessionMiddleware
from bottle import Bottle, HTTPResponse, request
from jumpscale.core.base import StoredFactory
from jumpscale.loader import j
from jumpscale.packages.auth.bottle.auth import SESSION_OPTS, get_user_info, login_required

app = Bottle()

FAUCET_WALLET = "faucet_wallet"
TRANSFER_AMOUNT = 1000


@app.route("/api/transfer", method="POST")
def transfer() -> str:

    request_data = j.data.serializers.json.loads(request.body.read())
    destination = request_data["destination"]

    distributor_wallet = j.clients.stellar.get(FAUCET_WALLET)

    asset = distributor_wallet.get_asset("TFT")  # asset.code:asset.issuer
    import nacl
    from nacl import hash

    hashed_wallet = hash.blake2b(destination.encode("utf-8"), encoder=nacl.encoding.RawEncoder)
    txes = distributor_wallet.list_transactions(address=destination)
    for tx in txes:
        if tx.memo_hash is not None:
            decoded_memo_hash = base64.b64decode(tx.memo_hash)
            if decoded_memo_hash == hashed_wallet:
                raise j.exceptions.Base("user already requested tokens")

    try:
        distributor_wallet.transfer(
            destination_address=destination,
            amount=TRANSFER_AMOUNT,
            asset=f"{asset.code}:{asset.issuer}",
            memo_hash=hashed_wallet,
        )
    except Exception as e:
        raise j.exceptions.Base(e)

    return j.data.serializers.json.dumps({"data": "Transfer complete"})


app = SessionMiddleware(app, SESSION_OPTS)
