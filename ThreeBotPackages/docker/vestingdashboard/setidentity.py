#!/usr/bin/env python
import os
from jumpscale.loader import j


explorer_api_urls={
    "TEST":"https://explorer.testnet.grid.tf/api/v1",
    "STD":"https://explorer.grid.tf/api/v1",
}

def set_identity():
    network=os.environ.get("TFT_SERVICES_NETWORK", "TEST")
    j.core.identity.new("vestingdashboard","vestingdashboard.3bot",email="vestingdashboard@threefold.tech",explorer_url=explorer_api_urls[network]).save()





if __name__ == "__main__":
    set_identity()