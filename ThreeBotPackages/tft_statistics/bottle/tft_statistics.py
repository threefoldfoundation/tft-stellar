import datetime
import os
import sys
import os
import stellar_sdk

from beaker.middleware import SessionMiddleware
from bottle import Bottle, request, HTTPError, response

from jumpscale.loader import j
from jumpscale.packages.auth.bottle.auth import SESSION_OPTS


current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../../../lib/stats/")

from stats import StatisticsCollector

TFT_ISSUER = "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47"

app = Bottle()


def get_cache_time():
    caching_time = os.environ.get("TFTSTATISTICS_CACHETIME", "600")
    return int(caching_time)


def _get_foundation_wallets() -> list:
    redis = j.clients.redis.get("redis_instance")
    cached_data = redis.get(f"foundationaccounts-raw")
    if cached_data:
        return j.data.serializers.json.loads(cached_data)

    foundationwallets_path = os.environ.get("TFACCOUNTS", None)
    if not foundationwallets_path:
        return []
    foundationaccounts = j.data.serializers.json.load_from_file(foundationwallets_path)
    redis.set(f"foundationaccounts-raw", j.data.serializers.json.dumps(foundationaccounts), ex=get_cache_time())
    return foundationaccounts


def _get_not_liquid_foundation_addesses() -> list:
    result = []
    for category in _get_foundation_wallets():
        result += [account["address"] for account in category["wallets"] if not account["liquid"]]
    return result


@app.route("/api/foundationaccounts")
def get_foundation_wallets():
    response.content_type = "application/json"
    redis = j.clients.redis.get("redis_instance")
    cached_data = redis.get(f"foundationaccounts-detailed")
    if cached_data:
        return cached_data
    foundation_wallets = _get_foundation_wallets()

    horizon_server = stellar_sdk.Server("https://horizon.stellar.org")
    for category in foundation_wallets:
        for foundation_wallet in category["wallets"]:
            endpoint = horizon_server.accounts().account_id(foundation_wallet["address"])
            account_data = endpoint.call()
            tftbalances = [
                balance["balance"]
                for balance in account_data["balances"]
                if balance.get("asset_code") == "TFT" and balance.get("asset_issuer") == TFT_ISSUER
            ]
            foundation_wallet["TFT"] = tftbalances[0] if tftbalances else "0.0"
            foundation_wallet["signers"] = [signer["key"] for signer in account_data["signers"]]
            required_signatures = account_data["thresholds"]["med_threshold"]
            foundation_wallet["required_signatures"] = required_signatures if required_signatures != 0 else 1
    res = j.data.serializers.json.dumps(foundation_wallets)
    redis.set(f"foundationaccounts-detailed", res, ex=get_cache_time())
    return res


@app.route("/api/stats")
def get_stats():
    """Statistics about TFT and TFTA

    Args:
        network (str ["test", "public"], optional): Defaults to "public".
        tokencode (str ["TFT", "TFTA"], optional): Defaults to "TFT".
        detailed (bool, optional): Defaults to False.
    """
    query_params = request.query.decode()
    network = query_params.get("network", "public")
    tokencode = query_params.get("tokencode", "TFT")
    detailed = j.data.serializers.json.loads(query_params.get("detailed", "false"))
    res = {}

    # cache the request in local redis
    redis = j.clients.redis.get("redis_instance")
    cached_data = redis.get(f"{network}-{tokencode}-{detailed}")
    if cached_data:
        return cached_data

    collector = StatisticsCollector(network)

    if detailed:
        foundation_wallets = _get_foundation_wallets()
        foundation_addresses = []
        for category in foundation_wallets:
            foundation_addresses += [account["address"] for account in category["wallets"]]
    else:
        foundation_addresses = _get_not_liquid_foundation_addesses()

    stats = collector.getstatistics(tokencode, foundation_addresses, detailed)
    res["total_tokens"] = f"{stats['total']:,.7f}"
    res["total_accounts"] = f"{stats['num_accounts']}"
    res["total_locked_tokens"] = f"{stats['total_locked']:,.7f}"
    res["total_vested_tokens"] = f"{stats['total_vested']:,.7f}"
    if not detailed:
        res["total_illiquid_foundation_tokens"] = f"{stats['total_foundation']:,.7f}"
        total_liquid_tokens = stats["total"] - stats["total_locked"] - stats["total_vested"] - stats["total_foundation"]
        res["total_liquid_tokens"] = f"{total_liquid_tokens:,.7f}"
    else:
        foundation_amounts = {account["account"]: account["amount"] for account in stats["foundation"]}
        foundation_liquid_amount = 0.0
        foundation_illiquid_amount = 0.0

        for category in foundation_wallets:
            for foundation_wallet in category["wallets"]:
                amount = foundation_amounts.get(foundation_wallet["address"], 0)
                foundation_wallet["amount"] = f"{amount:,.7f}"
                if foundation_wallet["liquid"]:
                    foundation_liquid_amount += amount
                else:
                    foundation_illiquid_amount += amount

        res["total_liquid_foundation_tokens"] = f"{foundation_liquid_amount:,.7f}"
        res["total_illiquid_foundation_tokens"] = f"{foundation_illiquid_amount:,.7f}"
        total_liquid_tokens = (
            stats["total"] - stats["total_locked"] - stats["total_vested"] - foundation_illiquid_amount
        )
        res["total_liquid_tokens"] = f"{total_liquid_tokens:,.7f}"
        res["foundation_accounts_info"] = foundation_wallets
        res["locked_tokens_info"] = []
        for locked_amount in stats["locked"]:
            res["locked_tokens_info"].append(
                f"{locked_amount['amount']:,.7f} locked until {datetime.datetime.fromtimestamp(locked_amount['until'])}"
            )
    results = j.data.serializers.json.dumps(res)
    redis.set(f"{network}-{tokencode}-{detailed}", results, ex=get_cache_time())

    return results


@app.route("/api/total_tft")
def total_tft():
    query_params = request.query.decode()
    network = query_params.get("network", "public")
    tokencode = query_params.get("tokencode", "TFT")

    # cache the request in local redis
    redis = j.clients.redis.get("redis_instance")
    cached_data = redis.get(f"{network}-{tokencode}-total_tft")
    if cached_data:
        return cached_data

    collector = StatisticsCollector(network)
    stats = collector.getstatistics(tokencode, [], False)

    total = stats["total"]
    redis.set(f"{network}-{tokencode}-total_tft", total, ex=get_cache_time())
    return f"{total}"


@app.route("/api/total_unlocked_tft")
def total_unlocked_tft():
    query_params = request.query.decode()
    network = query_params.get("network", "public")
    tokencode = query_params.get("tokencode", "TFT")

    # cache the request in local redis
    redis = j.clients.redis.get("redis_instance")
    cached_data = redis.get(f"{network}-{tokencode}-total_unlocked_tft")
    if cached_data:
        return cached_data

    collector = StatisticsCollector(network)
    stats = collector.getstatistics(tokencode, _get_not_liquid_foundation_addesses(), False)

    total_tft = stats["total"]
    total_locked_tft = stats["total_locked"]
    total_vested_tft = stats["total_vested"]
    total_foundation = stats["total_foundation"]
    total_unlocked_tft = total_tft - total_locked_tft - total_vested_tft - total_foundation

    redis.set(f"{network}-{tokencode}-total_unlocked_tft", total_unlocked_tft, ex=get_cache_time())
    return f"{total_unlocked_tft}"


@app.route("/api/account/<address>")
def get_address_info(address):
    global get_address_info_wallet

    def balances_to_reponse(balances):
        return [
            {
                "amount": balance.balance,
                "asset": f"{balance.asset_code}{(':'+balance.asset_issuer) if balance.asset_issuer else ''}",
            }
            for balance in balances
        ]

    if not "get_address_info_wallet" in globals():
        get_address_info_wallet = j.clients.stellar.new(j.data.random_names.random_name(), network="STD")
    try:
        data = get_address_info_wallet.get_balance(address)
    except stellar_sdk.exceptions.BadRequestError as e:
        if e.extras:
            if e.extras.get("invalid_field") == "account_id":
                return HTTPError(status=j.tools.http.status_codes.codes.BAD_REQUEST)
    except stellar_sdk.exceptions.NotFoundError:
        return HTTPError(status=j.tools.http.status_codes.codes.NOT_FOUND)

    response = {}
    response["address"] = address
    response["balances"] = balances_to_reponse(data.balances)

    if data.vesting_accounts:
        vesting_accounts = []
        for vesting_account in data.vesting_accounts:
            vesting_accounts.append(
                {
                    "address": vesting_account.address,
                    "balances": balances_to_reponse(vesting_account.balances),
                    "vestingscheme": vesting_account.scheme,
                }
            )

        response["vesting_accounts"] = vesting_accounts

    if data.escrow_accounts:
        locked_amounts = []
        for locked_amount in data.escrow_accounts:
            locked_amounts.append(
                {
                    "address": locked_amount.address,
                    "locked_until": datetime.datetime.fromtimestamp(locked_amount.unlock_time).isoformat(),
                    "balances": balances_to_reponse(locked_amount.balances),
                }
            )

        response["locked_amounts"] = locked_amounts

    return response


app = SessionMiddleware(app, SESSION_OPTS)
