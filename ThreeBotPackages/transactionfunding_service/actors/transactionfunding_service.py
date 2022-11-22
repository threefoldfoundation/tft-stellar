import os
import sys
import random
import time
import stellar_sdk

from jumpscale.loader import j
from jumpscale.servers.gedis.baseactor import BaseActor, actor_method

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/sals/")
from transactionfunding_sal import ASSET_FEES, WALLET_NAME, NUMBER_OF_SLAVES, fund_if_needed


_HORIZON_NETWORKS = {"TEST": "https://horizon-testnet.stellar.org", "STD": "https://horizon.stellar.org"}

_MAX_FEE=1000000

def asset_to_full_asset_string(asset: stellar_sdk.Asset) -> str:
    if asset.is_native():
        return "XLM"
    return f"{asset.code.upper()}:{asset.issuer}"


def is_signed_transaction(txe: stellar_sdk.TransactionEnvelope) -> bool:
    return len(txe.signatures) > 0


class Transactionfunding_service(BaseActor):
    def _get_network(self) -> str:
        return str(j.clients.stellar.get(WALLET_NAME).network.value)

    def _get_network_passphrase(self) -> str:
        if self._get_network() == "TEST":
            return stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
        return stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE

    def _get_asset_fees(self) -> dict:
        return ASSET_FEES[self._get_network()]

    def _get_horizon_server(self):

        return stellar_sdk.Server(horizon_url=_HORIZON_NETWORKS[self._get_network()])

    def _create_fee_payment_operation(self, from_address, asset):
        condition = [
            condition for condition in self.conditions() if condition["asset"] == asset_to_full_asset_string(asset)
        ][0]
        fee_amount = condition["fee_fixed"]
        fee_target = condition["fee_account_id"]

        return stellar_sdk.Payment(fee_target, asset, fee_amount, from_address)

    def _get_slave_fundingwallet(self):
        earliest_sequence = int(time.time()) - 60  # 1 minute
        least_recently_used_wallet = None
        # Loop over the slavewallets, starting at a random one
        startindex = random.randrange(0, NUMBER_OF_SLAVES)
        r = range(startindex, startindex + NUMBER_OF_SLAVES)
        for slaveindex in [i % NUMBER_OF_SLAVES for i in r]:
            walletname = WALLET_NAME + "_" + str(slaveindex)
            if walletname not in j.clients.stellar.list_all():
                return None
            wallet = j.clients.stellar.get(walletname)
            a = wallet.load_account()
            if a.last_created_sequence_is_used:
                return wallet
            else:
                if wallet.sequencedate < earliest_sequence:
                    earliest_sequence = wallet.sequencedate
                    least_recently_used_wallet = wallet
        if not least_recently_used_wallet:  # Can not happen
            raise j.exceptions.Value("Service Unavailable")
        return least_recently_used_wallet

    @actor_method
    def conditions(self) -> list:
        main_wallet = j.clients.stellar.get(WALLET_NAME)
        fee_target = main_wallet.address
        asset_fees = self._get_asset_fees()
        conditions = [
            {"asset": asset, "fee_account_id": fee_target, "fee_fixed": fee} for asset, fee in asset_fees.items()
        ]
        return conditions

    def _fee_bump(self, txe: stellar_sdk.TransactionEnvelope) -> dict:

        funding_wallet = self._get_slave_fundingwallet()

        source_public_kp = stellar_sdk.Keypair.from_public_key(funding_wallet.address)
        source_signing_kp = stellar_sdk.Keypair.from_secret(funding_wallet.secret)


        fb_txe = stellar_sdk.TransactionBuilder.build_fee_bump_transaction(
            source_public_kp,
            base_fee=_MAX_FEE,
            inner_transaction_envelope=txe,
            network_passphrase=self._get_network_passphrase(),
        )
        fb_txe.sign(source_signing_kp)

        horizon_server = self._get_horizon_server()
        try:
            response = horizon_server.submit_transaction(fb_txe)
        except stellar_sdk.exceptions.BadRequestError as ex:
            result_codes = ex.extras["result_codes"]
            if result_codes.get("transaction") == "tx_fee_bump_inner_failed":
                error_data = j.data.serializers.json.dumps({"operations": result_codes.get("operations", [])})
                raise j.exceptions.Value(error_data)
            raise ex

        fund_if_needed(funding_wallet.instance_name)

        return {"transactionhash": response["hash"]}

    def _append_fee_payment(self, txe: stellar_sdk.TransactionEnvelope) -> dict:

        txe.transaction.operations.append(
            self._create_fee_payment_operation(
                txe.transaction.operations[0].source, txe.transaction.operations[0].asset
            )
        )

        txe.transaction.fee = _MAX_FEE

        funding_wallet = self._get_slave_fundingwallet()

        source_public_kp = stellar_sdk.Keypair.from_public_key(funding_wallet.address)
        source_signing_kp = stellar_sdk.Keypair.from_secret(funding_wallet.secret)

        source_account = funding_wallet.load_account()
        source_account.increment_sequence_number()
        txe.transaction.source = source_public_kp

        txe.transaction.sequence = source_account.sequence
        txe.sign(source_signing_kp)

        transaction_xdr = txe.to_xdr()

        fund_if_needed(funding_wallet.instance_name)

        return {"transaction_xdr": transaction_xdr}

    @actor_method
    def fund_transaction(self, transaction: str = None, args: dict = None) -> dict:
        # Backward compatibility with jsx service for request body {'args': {'transaction': <transaction>}}
        if not transaction and not args:
            raise j.exceptions.Value(f"missing a required argument: 'transaction'")
        if args:
            try:
                if "transaction" in args:
                    transaction = args.get("transaction", None)
                else:
                    raise j.exceptions.Value(f"missing a required argument: 'transaction' in args dict")
            except j.data.serializers.json.json.JSONDecodeError:
                pass

        txe = stellar_sdk.transaction_envelope.TransactionEnvelope.from_xdr(
            transaction + "===", self._get_network_passphrase()
        )

        asset_fees = self._get_asset_fees()

        if len(txe.transaction.operations) == 0:
            raise j.exceptions.NotFound("No operations in the supplied transaction")

        if is_signed_transaction(txe):
            return self._fee_bump(txe)

        asset = None
        for op in txe.transaction.operations:
            if type(op) != stellar_sdk.Payment:
                raise j.exceptions.Value("Only payment operations are supported")
            full_asset_code = asset_to_full_asset_string(op.asset)

            if full_asset_code not in asset_fees:
                raise j.exceptions.Value("Unsupported asset")
            if asset:
                if asset != op.asset:
                    raise j.exceptions.Value("Only 1 type of asset is supported")
            else:
                asset = op.asset

        return self._append_fee_payment(txe)


Actor = Transactionfunding_service
