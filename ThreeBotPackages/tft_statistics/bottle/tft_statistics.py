import datetime
import os
import sys

from beaker.middleware import SessionMiddleware
from bottle import Bottle, request

from jumpscale.loader import j
from jumpscale.packages.auth.bottle.auth import SESSION_OPTS


current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../../../lib/stats/")

from stats import StatisticsCollector

app = Bottle()


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
    stats = collector.getstatistics(tokencode, detailed)
    res["total_tokens"] = f"{stats['total']:,.7f}"
    res["total_accounts"] = f"{stats['num_accounts']}"
    res["total_locked_tokens"] = f"{stats['total_locked']:,.7f}"
    if detailed:
        res["locked_tokens_info"] = []
        for locked_amount in stats["locked"]:
            res["locked_tokens_info"].append(
                f"{locked_amount['amount']:,.7f} locked until {datetime.datetime.fromtimestamp(locked_amount['until'])}"
            )
    results = j.data.serializers.json.dumps(res)
    redis.set(f"{network}-{tokencode}-{detailed}", results, ex=600)

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
    stats = collector.getstatistics(tokencode, False)

    total = stats["total"]
    redis.set(f"{network}-{tokencode}-total_tft", total, ex=600)
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
    stats = collector.getstatistics(tokencode, False)

    total_tft = stats["total"]
    total_locked_tft = stats["total_locked"]
    total_unlocked_tft = total_tft - total_locked_tft

    redis.set(f"{network}-{tokencode}-total_unlocked_tft", total_unlocked_tft, ex=600)
    return f"{total_unlocked_tft}"


app = SessionMiddleware(app, SESSION_OPTS)
