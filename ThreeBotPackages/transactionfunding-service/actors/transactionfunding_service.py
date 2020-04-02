from Jumpscale import j


_TFT_FULL_ASSETCODES = {
    "TEST": "TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3",
    "STD": "TFT:GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
}
_HORIZON_NETWORKS = {"TEST": "https://horizon-testnet.stellar.org", "STD": "https://horizon.stellar.org"}


class transactionfunding_service(j.baseclasses.threebot_actor):
    def _get_horizon_server(self, network):
        import stellar_sdk

        return stellar_sdk.Server(horizon_url=_HORIZON_NETWORKS[str(network)])

    def _get_tft_asset(self, network):
        import stellar_sdk

        fullcode = _TFT_FULL_ASSETCODES[str(network)]
        split_code = fullcode.split(":")
        return stellar_sdk.Asset(split_code[0], split_code[1])

    def _create_tft_fee_payment(self, from_address, destination, network):
        import stellar_sdk

        asset = self._get_tft_asset(network)
        return stellar_sdk.Payment(destination, asset, "0.1", from_address)

    @j.baseclasses.actor_method
    def fund_transaction(self, transaction, schema_out=None, user_session=None):

        funding_wallet = j.clients.stellar.get("txfundingwallet")

        # after getting the wallet, the required imports are available
        import stellar_sdk

        if str(funding_wallet.network) == "TEST":
            network_passphrase = stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
        else:
            network_passphrase = stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE
        txe = stellar_sdk.transaction_envelope.TransactionEnvelope.from_xdr(transaction, network_passphrase)
        source_public_kp = stellar_sdk.Keypair.from_public_key(funding_wallet.address)
        source_signing_kp = stellar_sdk.Keypair.from_secret(funding_wallet.secret)
        horizon_server = self._get_horizon_server(funding_wallet.network)
        base_fee = horizon_server.fetch_base_fee()

        source_account = horizon_server.load_account(funding_wallet.address)
        source_account.increment_sequence_number()
        txe.transaction.source = source_public_kp

        if len(txe.transaction.operations) == 0:
            raise j.exceptions.Base("No operations in the supplied transaction")
        txe.transaction.operations.append(
            self._create_tft_fee_payment(
                txe.transaction.operations[0].source, funding_wallet.address, funding_wallet.network
            )
        )

        txe.transaction.fee = base_fee * len(txe.transaction.operations)

        txe.transaction.sequence = source_account.sequence
        txe.sign(source_signing_kp)
        return txe.to_xdr()
