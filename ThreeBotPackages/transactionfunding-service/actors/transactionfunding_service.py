from Jumpscale import j
import random
import time

_TFT_ISSUERS = {
    "TEST": "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3",
    "STD": "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
}

_FREETFT_ISSUERS = {
    "TEST": "GBLDUINEFYTF7XEE7YNWA3JQS4K2VD37YU7I2YAE7R5AHZDKQXSS2J6R",
    "STD": "GCBGS5TFE2BPPUVY55ZPEMWWGR6CLQ7T6P46SOFGHXEBJ34MSP6HVEUT",
}

_ASSET_ISSUERS = {"TFT": _TFT_ISSUERS, "FreeTFT": _FREETFT_ISSUERS}

_HORIZON_NETWORKS = {"TEST": "https://horizon-testnet.stellar.org", "STD": "https://horizon.stellar.org"}


class transactionfunding_service(j.baseclasses.threebot_actor):
    def _get_horizon_server(self, network):
        import stellar_sdk

        return stellar_sdk.Server(horizon_url=_HORIZON_NETWORKS[str(network)])

    def _create_fee_payment(self, from_address, asset):
        main_walletname = self.package.install_kwargs.get("wallet", "txfundingwallet")
        fee_target = j.clients.stellar.get(main_walletname).address

        import stellar_sdk

        return stellar_sdk.Payment(fee_target, asset, "0.1", from_address)

    def _get_fundingwallet(self):
        main_walletname = self.package.install_kwargs.get("wallet", "txfundingwallet")

        nr_of_slaves = self.package.install_kwargs.get("slaves", 30)
        earliest_sequence = int(time.time()) - 60  # 1 minute
        least_recently_used_wallet = None
        # Loop over the slavewallets, starting at a random one
        startindex = random.randrange(0, nr_of_slaves)
        r = range(startindex, startindex + nr_of_slaves)
        for slaveindex in [i % nr_of_slaves for i in r]:
            walletname = main_walletname + "_" + str(slaveindex)
            wallet = j.clients.stellar.get(walletname)
            a = wallet.load_account()
            if a.last_created_sequence_is_used:
                return wallet
            else:
                if wallet.sequencedate < earliest_sequence:
                    earliest_sequence = wallet.sequencedate
                    least_recently_used_wallet = wallet
        return least_recently_used_wallet

    @j.baseclasses.actor_method
    def fund_transaction(self, transaction, schema_out=None, user_session=None):
        """
        ```in
        transaction = (S)
        ```

        ```out
        transaction_xdr = (S)
        ```
        """

        funding_wallet = self._get_fundingwallet()
        if not funding_wallet:
            raise j.exceptions.Base("Service Unavailable")

        # after getting the wallet, the required imports are available
        import stellar_sdk

        if str(funding_wallet.network) == "TEST":
            network_passphrase = stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
        else:
            network_passphrase = stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE
        txe = stellar_sdk.transaction_envelope.TransactionEnvelope.from_xdr(transaction, network_passphrase)

        source_public_kp = stellar_sdk.Keypair.from_public_key(funding_wallet.address)
        source_signing_kp = stellar_sdk.Keypair.from_secret(funding_wallet.secret)
        

        if len(txe.transaction.operations) == 0:
            raise j.exceptions.Base("No operations in the supplied transaction")
        asset = None
        for op in txe.transaction.operations:
            if type(op) != stellar_sdk.operation.Payment:
                raise j.exceptions.Base("Only payment operations are supported")
            if op.asset.code not in _ASSET_ISSUERS:
                raise j.exceptions.Base("Unsupported asset")
            if _ASSET_ISSUERS[op.asset.code][str(funding_wallet.network)] != op.asset.issuer:
                raise j.exceptions.Base("Unsupported asset")
            if asset:
                if asset != op.asset:
                    raise j.exceptions.Base("Only 1 type of asset is supported")
            else:
                asset = op.asset

        txe.transaction.operations.append(self._create_fee_payment(txe.transaction.operations[0].source, asset))

        # set the necessary fee
        horizon_server = self._get_horizon_server(funding_wallet.network)
        base_fee = horizon_server.fetch_base_fee()
        txe.transaction.fee = base_fee * len(txe.transaction.operations)

        
        source_account = funding_wallet.load_account()
        source_account.increment_sequence_number()
        txe.transaction.source = source_public_kp

        txe.transaction.sequence = source_account.sequence
        txe.sign(source_signing_kp)

        out = schema_out.new()
        out.transaction_xdr = txe.to_xdr()
        return out
