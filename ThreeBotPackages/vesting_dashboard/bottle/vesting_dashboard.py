import pdb
from beaker.middleware import SessionMiddleware
from bottle import Bottle, request, HTTPResponse, abort, redirect
import os, sys

from jumpscale.loader import j
from jumpscale.packages.auth.bottle.auth import SESSION_OPTS, login_required, get_user_info
from jumpscale.core.base import StoredFactory

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../models/")
from models import VestingEntry

vesting_entry_model = StoredFactory(VestingEntry)
vesting_entry_model.always_reload = True


app = Bottle()

wallet_name = "vesting_temp_wallet"
vesting_service_url = {
    "testnet": "https://testnet.threefold.io/threefoldfoundation/vesting_service",
    "mainnet": "https://tokenservices.threefold.io/threefoldfoundation/vesting_service",
}


def _get_balance_details(account):
    balance_details = []
    balances = account.balances

    for b in balances:
        balance_details.append({"asset": b.asset_code, "issuer": b.asset_issuer, "balance": b.balance})

    return balance_details


@app.route("/api/account/create", method="POST")
@login_required
def create_escrow_account():
    data = j.data.serializers.json.loads(request.body.read())
    user_info = j.data.serializers.json.loads(get_user_info())
    username = user_info["username"].replace(".3bot", "")
    owner_address = data["owner_address"]
    if not owner_address:
        abort(400, "Error: owner_address param missing")
    # To be added to limit user to one vesting account creation
    # _, vesting_check_count, _ = vesting_entry_model.find_many(username=username)
    # if vesting_check_count > 0:
    #     abort(400, "Warning: User can add currently only add one vesting account")

    _, vesting_check_count, _ = vesting_entry_model.find_many(
        f"{username}_{owner_address}", owner_address=owner_address
    )
    if vesting_check_count > 0:
        abort(400, "Warning: User already created vesting account for this address")

    vesting_response = j.tools.http.get(
        url=f"{vesting_service_url['testnet']}/create_vesting_account",
        data=j.data.serializers.json.dumps({"owner_address": owner_address}),
        headers={"Content-Type": "application/json"},
    )
    if vesting_response.status_code != 200:
        abort(vesting_response.status_code, "Error occured creating vesting account")

    vesting_address = vesting_response.json()["address"]
    vesting_entry = vesting_entry_model.new(f"{username}_{owner_address}")
    vesting_entry.username = username
    vesting_entry.owner_address = owner_address
    vesting_entry.vesting_address = vesting_address
    vesting_entry.save()

    return j.data.serializers.json.dumps({"data": vesting_entry.to_dict()})


@app.route("/api/account/list", method="GET")
@login_required
def list_vesting_accounts():
    user_info = j.data.serializers.json.loads(get_user_info())
    username = user_info["username"].replace(".3bot", "")

    _, _, vesting_accounts = vesting_entry_model.find_many(username=username)

    tmp_wallet = j.clients.stellar.get(wallet_name)
    result_payments = []
    for account in vesting_accounts:
        vesting_address = account.vesting_address

        payments = tmp_wallet.list_payments(vesting_address)
        transactions = []
        for payment in payments:
            if payment.balance.asset_code != "TFT" or payment.payment_type != "payment":
                continue
            time = j.data.time.get(payment.created_at).timestamp
            transactions.append(
                {"timestamp": time, "amount": payment.balance.balance, "transaction_hash": payment.transaction_hash}
            )

        account_balances = []
        account_balances = _get_balance_details(tmp_wallet.get_balance(account.owner_address))

        locked_balances_details = []
        locked_accounts = tmp_wallet.get_balance(account.owner_address).escrow_accounts
        for locked_account in locked_accounts:
            locked_account_balances = _get_balance_details(locked_account)
            locked_balances_details.append(
                {"vesting": locked_account.address, "lockedbalances": locked_account_balances}
            )

        result_payments.append(
            {
                "owner": account.owner_address,
                "transactions": transactions,
                "vesting": account.vesting_address,
                "balances": account_balances,
                "locked": locked_balances_details,
            }
        )

    return j.data.serializers.json.dumps({"data": result_payments})


app = SessionMiddleware(app, SESSION_OPTS)
