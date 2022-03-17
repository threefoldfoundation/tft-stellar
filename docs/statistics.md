# Statistics

## Detailed api

On production, this api is available at [https://statsdata.threefoldtoken.com/stellar_stats/api/stats](https://statsdata.threefoldtoken.com/stellar_stats/api/stats)

- `total_locked_tokens`: Sum of all time locked tokens in `locked_tokens_info`

## Summarized api's

### Total unlocked

On production, this api is available at [https://statsdata.threefoldtoken.com/stellar_stats/api/total_unlocked_tft](https://statsdata.threefoldtoken.com/stellar_stats/api/total_unlocked_tft).

This is calculated from the detailed api.

total_tokens - total_locked_tokens - total_vested_tokens - total_illiquid_foundation_tokens
