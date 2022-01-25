# Stellar statistics

## Install the package

```python3
JS-NG> server = j.servers.threebot.get("default")
JS-NG> server.packages.add(giturl="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/tft_statistics")
JS-NG> server.save()
JS-NG> server.start()
```

- On production add the domain in the `package.toml` currently is set to `statsdata.threefoldtoken.com`

## Endpoints

- `https://<host>/tft_statistics/api/stats`
    
    Query params:
    - network: (str ["test", "public"], optional): Defaults to "public".
    - tokencode: (str ["TFT", "TFTA"], optional): Defaults to "TFT".
    - detailed: (bool, optional): Defaults to False.

- `https://<host>/tft_statistics/api/total_tft`
- `https://<host>/tft_statistics/api/total_unlocked_tft`
- `https://<host>/tft_statistics/api/foundationaccounts`: Foundation addresses and their description
- `https://<host>/tft_statistics/api/account/<address>` : get the details of an account

## Examples

- https://localhost/tft_statistics/api/stats
- https://localhost/tft_statistics/api/stats?tokencode=TFT
- https://localhost/tft_statistics/api/stats?tokencode=TFTA
- https://localhost/tft_statistics/api/foundationaccounts
- https://localhost/tft_statistics/api/total_tft
- https://localhost/tft_statistics/api/total_unlocked_tft

## Deployed examples

## Test environment

- `https://statsdata.testnet.threefold.io/stellar_stats/api/stats`
- `https://statsdata.testnet.threefold.io/stellar_stats/api/foundationaccounts`
- `https://statsdata.testnet.threefold.io/stellar_stats//api/account/<address>`

## Production environment

- `https://statsdata.threefoldtoken.com/stellar_stats/api/stats`
- `https://statsdata.threefoldtoken.com/stellar_stats/api/foundationaccounts`
- `https://statsdata.threefold.io/stellar_stats//api/account/<address>`
