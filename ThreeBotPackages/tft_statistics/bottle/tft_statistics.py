import datetime
import stellar_sdk

from bottle import Bottle, request, HTTPError, response

from jumpscale.loader import j


app = Bottle()


@app.route("/api/foundationaccounts")
def get_foundation_wallets():
    response.content_type = "application/json"

    redis = j.clients.redis.get("redis_instance")

    cached_data = redis.get(f"foundationaccounts-detailed")
    if cached_data:
        return cached_data

    return HTTPError(status=j.tools.http.status_codes.codes.SERVICE_UNAVAILABLE)


@app.route("/api/stats")
def get_stats():
    """Statistics about TFT and TFTA

    Args:
        tokencode (str ["TFT", "TFTA"], optional): Defaults to "TFT".
    """
    query_params = request.query.decode()
    tokencode = query_params.get("tokencode", "TFT")

    if tokencode not in ["TFT", "TFTA"]:
        return HTTPError(status=j.tools.http.status_codes.codes.BAD_REQUEST)

    # cache the request in local redis via service
    redis = j.clients.redis.get("redis_instance")
    cached_data = redis.get(tokencode)

    if cached_data:
        return cached_data

    return HTTPError(status=j.tools.http.status_codes.codes.SERVICE_UNAVAILABLE)


@app.route("/api/total_tft")
def total_tft():
    query_params = request.query.decode()
    tokencode = query_params.get("tokencode", "TFT")

    if tokencode not in ["TFT", "TFTA"]:
        return HTTPError(status=j.tools.http.status_codes.codes.BAD_REQUEST)

    # cache the request in local redis
    redis = j.clients.redis.get("redis_instance")
    cached_data = j.data.serializers.json.loads(redis.get(tokencode))

    if cached_data.get("total_tokens"):
        return cached_data.get("total_tokens").replace(",", "")

    return HTTPError(status=j.tools.http.status_codes.codes.SERVICE_UNAVAILABLE)


@app.route("/api/total_supply")
def total_supply():
    # just adds TFT + TFTA on Stellar to give a total supply figure.
    total_supply = 0
    redis = j.clients.redis.get("redis_instance")
    for tokencode in ["TFT", "TFTA"]:
        if cached_data := redis.get(tokencode):
            token_data = j.data.serializers.json.loads(cached_data)
            if token_data.get("total_tokens"):
                total_supply += float(token_data["total_tokens"].replace(",", ""))
            else:
                return HTTPError(status=j.tools.http.status_codes.codes.SERVICE_UNAVAILABLE)
        else:
            return HTTPError(status=j.tools.http.status_codes.codes.SERVICE_UNAVAILABLE)
    return str(total_supply)


@app.route("/api/total_unlocked_tft")
def total_unlocked_tft():
    query_params = request.query.decode()
    tokencode = query_params.get("tokencode", "TFT")

    if tokencode not in ["TFT", "TFTA"]:
        return HTTPError(status=j.tools.http.status_codes.codes.BAD_REQUEST)

    # cache the request in local redis
    redis = j.clients.redis.get("redis_instance")
    cached_data = j.data.serializers.json.loads(redis.get(tokencode))
    if cached_data:
        total_tokens = float(cached_data["total_tokens"].replace(",", ""))
        total_locked_tokens = float(cached_data["total_locked_tokens"].replace(",", ""))
        total_vested_tokens = float(cached_data["total_vested_tokens"].replace(",", ""))
        total_foundation = float(cached_data["total_illiquid_foundation_tokens"].replace(",", ""))
        total_unlocked_tokens = total_tokens - total_locked_tokens - total_vested_tokens - total_foundation

        return str(total_unlocked_tokens)

    return HTTPError(status=j.tools.http.status_codes.codes.SERVICE_UNAVAILABLE)


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
        free_locked_amounts = []
        for locked_amount in data.escrow_accounts:
            locked_amount_response = {
                "address": locked_amount.address,
                "balances": balances_to_reponse(locked_amount.balances),
            }
            if locked_amount.unlock_time is not None:
                locked_amount_response["locked_until"] = datetime.datetime.fromtimestamp(
                    locked_amount.unlock_time
                ).isoformat()
                locked_amounts.append(locked_amount_response)
            else:
                free_locked_amounts.append(locked_amount_response)
        if locked_amounts:
            response["locked_amounts"] = locked_amounts
        if free_locked_amounts:
            response["free_amounts"] = free_locked_amounts

    return response

