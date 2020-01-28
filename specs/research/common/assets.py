
import stellar_sdk

def asset_from_full_string(full_asset_string):
    split_asset= full_asset_string.split(':',1)
    asset_code=split_asset[0]
    asset_issuer=split_asset[1]

    asset=stellar_sdk.Asset(asset_code,asset_issuer)
    return asset