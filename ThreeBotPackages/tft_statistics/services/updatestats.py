import datetime
import os
import sys

from jumpscale.loader import j
from jumpscale.tools.servicemanager.servicemanager import BackgroundService

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../../")

from tft_statistics.sals.stats_sals import (
    update_foundation_wallets_data,
    update_stats,
    update_total_tft,
    update_total_unlocked_tft,
)


class UpdateTokensStats(BackgroundService):
    def __init__(self, interval=60 * 60, *args, **kwargs):
        """Update tokens stats every 60 minutes
        """
        super().__init__(interval, *args, **kwargs)
        self.schedule_on_start = True

    def job(self):
        try:
            # update foundation wallets
            j.logger.info(f"Updating foundation wallets")
            foundation_wallets = update_foundation_wallets_data()
            j.logger.debug(f"Foundation wallets updated successfully {foundation_wallets}")

            # update total tft & tfta total tokens
            j.logger.info("Updating total TFT")
            total_tft = update_total_tft(tokencode="TFT")
            j.logger.debug(f"Successfully updated total tft with: {total_tft}")

            j.logger.info("Updating total TFTA")
            total_tft = update_total_tft(tokencode="TFTA")
            j.logger.debug(f"Successfully updated total tft with: {total_tft}")

            # update total tft & tfta unlocked tokens
            j.logger.info("Updating total unlocked TFT")
            total_unlocked_tft = update_total_unlocked_tft(tokencode="TFT")
            j.logger.debug(f"Successfully updated total unlocked tft with: {total_unlocked_tft}")

            j.logger.info("Updating total TFTA")
            total_unlocked_tfta = update_total_unlocked_tft(tokencode="TFTA")
            j.logger.debug(f"Successfully updated total unlocked tft with: {total_unlocked_tfta}")

            # update tft & tfta stats
            j.logger.info("Updating statistics for TFT tokens")
            tft = update_stats(tokencode="TFT")
            j.logger.debug(f"Successfully updated TFT stats with: {tft}")

            j.logger.info("Updating statistics for TFTA tokens")
            tfta = update_stats(tokencode="TFTA")
            j.logger.debug(f"Successfully updated TFTA stats with: {tfta}")
        except Exception as e:
            j.logger.exception("Failed to update stats due to: ", exception=e)
            j.tools.alerthandler.alert_raise(
                app_name="Stats",
                category="internal_errors",
                message=f"Failed to update stats due due to error {str(e)}",
                alert_type="exception",
            )


service = UpdateTokensStats()
