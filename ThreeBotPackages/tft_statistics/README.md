# Stellar statistics

## Install the package

```python3
JS-NG> server = j.servers.threebot.get("default")
JS-NG> server.packages.add(giturl="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/tft_statistics")
JS-NG> server.save()
JS-NG> server.start()
```

- On production add the domain in the `package.toml` currently is set to `statsdata.threefoldtoken.com`

## Endpoint

https://<host>/tft_statistics/api/stats
https://<host>/tft_statistics/api/total_tft
https://<host>/tft_statistics/api/total_unlocked_tft

## Query params

- network: (str ["test", "public"], optional): Defaults to "public".
- tokencode: (str ["TFT", "TFTA"], optional): Defaults to "TFT".
- detailed: (bool, optional): Defaults to False.

## Examples

- https://localhost/tft_statistics/api/stats
- https://localhost/tft_statistics/api/stats?network=public
- https://localhost/tft_statistics/api/stats?tokencode=TFTA
- https://localhost/tft_statistics/api/stats?network=public&tokencode=TFTA
- https://localhost/tft_statistics/api/stats?network=public&tokencode=TFTA&detailed=true
- https://localhost/tft_statistics/api/total_tft
- https://localhost/tft_statistics/api/total_unlocked_tft
