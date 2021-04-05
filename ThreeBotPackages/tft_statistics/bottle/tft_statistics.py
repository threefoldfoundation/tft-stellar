import datetime
import os
import sys
import os

from beaker.middleware import SessionMiddleware
from bottle import Bottle, request

from jumpscale.loader import j
from jumpscale.packages.auth.bottle.auth import SESSION_OPTS


current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../../../lib/stats/")

from stats import StatisticsCollector

app = Bottle()


def get_cache_time():
    caching_time = os.environ.get("TFTSTATISTICS_CACHETIME", "600")
    return int(caching_time)


def _get_foundation_wallets() -> list:
    redis = j.clients.redis.get("redis_instance")
    cached_data = redis.get(f"foundationaccounts")
    if cached_data:
        return j.data.serializers.json.loads(cached_data)

    foundationwallets_path = os.environ.get("TFACCOUNTS", None)
    if not foundationwallets_path:
        return []
    foundationaccounts = j.data.serializers.json.load_from_file(foundationwallets_path)
    redis.set(f"foundationaccounts", j.data.serializers.json.dumps(foundationaccounts), ex=get_cache_time())
    return foundationaccounts


def _get_not_free_foundation_addesses() -> list:
    return [account["address"] for account in _get_foundation_wallets() if not account["free"]]


@app.route("/api/foundationaccounts")
def get_foundation_wallets():
    res = [
        {"address": account["address"], "description": account["description"]} for account in _get_foundation_wallets()
    ]
    results = j.data.serializers.json.dumps(res)
    return results


@app.route("/api/stats")
def get_stats():
    """Statistics about TFTand TFTA

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
    stats = collector.getstatistics(tokencode, _get_not_free_foundation_addesses(), detailed)
    res["total_tokens"] = f"{stats['total']:,.7f}"
    res["total_accounts"] = f"{stats['num_accounts']}"
    res["total_locked_tokens"] = f"{stats['total_locked']:,.7f}"
    res["total_vested_tokens"] = f"{stats['total_vested']:,.7f}"
    res["total_foundation_tokens"] = f"{stats['total_foundation']:,.7f}"
    total_liquid_tokens = stats["total"] - stats["total_locked"] - stats["total_vested"] - stats["total_foundation"]
    res["total_liquid_tokens"] = f"{total_liquid_tokens:,.7f}"
    if detailed:
        res["foundation_tokens_info"] = stats["foundation"]
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
    stats = collector.getstatistics(tokencode, _get_not_free_foundation_addesses(), False)

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
    stats = collector.getstatistics(tokencode, _get_not_free_foundation_addesses(), False)

    total_tft = stats["total"]
    total_locked_tft = stats["total_locked"]
    total_vested_tft = stats["total_vested"]
    total_foundation = stats["total_foundation"]
    total_unlocked_tft = total_tft - total_locked_tft - total_vested_tft - total_foundation

    redis.set(f"{network}-{tokencode}-total_unlocked_tft", total_unlocked_tft, ex=get_cache_time())
    return f"{total_unlocked_tft}"


app = SessionMiddleware(app, SESSION_OPTS)
