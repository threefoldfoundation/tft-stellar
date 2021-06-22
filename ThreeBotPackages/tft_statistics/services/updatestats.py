import datetime
import os
import sys

from jumpscale.loader import j
from jumpscale.tools.servicemanager.servicemanager import BackgroundService

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../../")

from tft_statistics.bottle.tft_statistics import _get_stats


class UpdateTokensStats(BackgroundService):
    def __init__(self, interval=60 * 60, *args, **kwargs):
        """Update tokens stats every 60 minutes
        """
        super().__init__(interval, *args, **kwargs)
        self.schedule_on_start = True

    def job(self):

        j.logger.info("Updating statistics for TFT tokens")
        tft = _get_stats(tokencode="TFT")
        j.logger.debug(f"Successfully updated TFT stats with: {tft}")
        j.logger.info("Updating statistics for TFTA tokens")
        tfta = _get_stats(tokencode="TFTA")
        j.logger.debug(f"Successfully updated TFTA stats with: {tfta}")


service = UpdateTokensStats()
