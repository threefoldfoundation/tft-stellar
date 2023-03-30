import os
import sys
import time

from urllib import parse

import stellar_sdk
from jumpscale.core.exceptions import JSException
from jumpscale.loader import j
from jumpscale.servers.gedis.baseactor import BaseActor, actor_method


current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../sals/")
from vesting_sal import get_wallet, get_unvesting_transactions


_TFT_ISSUERS = {
    "TEST": "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3",
    "STD": "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
}

_COSIGNERS = {
    "TEST": [
        "GB7Y3ZZVJ323L4ET35BAV6TYY76ANDMS75D5XQNPYJETMRPUM62VC7BN",
        "GCNQJSFACL2OOGDEBLPL4MFN7IS34RRH6YXZ7UZPSANJWWM6X67DGQXP",
        "GCN2ZZHY7PSXMHZYNYTK6O3TZSCSF2IAL4NH3QNXH2SCBXPVSWKAIY4Q",
        "GDUTZUYHLB5RYJSTWCBFTVBSOTCIXYZCZ2PTUMDFD3D2UIMZKRCOXG6R",
        "GAFHS5SEW3Y6BUX3FJ5OTVYP56BESVI3PNNKYNZPX2C5KTCXCZFHSADS",
        "GD2O7XG7CNLAKGZRQBMLOO3GRF3QVQF4ZPWO6ZC2V47WXXWQXEKSQWHQ",
        "GCHOZZFLIHA2T7YYSMUQU7CFKP2TQVL4WO75DGZLQBD7HGLT4D6Y3LC6",
        "GDLGTUQQOEY5IG2ZXIUYEJSU34BNRI43VJJNDSBPVMNYVHM2O4E72FGI",
        "GBUYN7WTS6VZG3JOHETOXXA7DVWVSO5SJBJOLVPDPIZ633JXIBSSMFBU",
    ],
    "STD": [
        "GARF35OFGW2XFHFG764UVO2UTUOSDRVL5DU7RXMM7JJJOSVWKK7GATXU",
        "GDORF4CKQ2GDOBXXU7R3EXV3XRN6LFCGNYTHMYXDPZ5NECZ6YZLJGAA2",
        "GDTTKKRECHQMYWJWKQ5UTONRMNK54WRN3PB4U7JZAPUHLPI75ALN7ORU",
        "GDSKTNDAIBUBGQZXEJ64F3P37T7Y45ZOZQCRZY2I46F4UT66KG4JJSOU",
        "GCHUIUY5MOBWOXEKZJEQU2DCUG4WHRXM4KAWCEUQK3NTQGBK5RZ6FQBR",
        "GDTFYNE5MKGFL625FNUQUHILILFNNRSRYAAXADFFLMOOF5E6V5FLLSBG",
        "GDOSJPACWZ2DWSDNNKCVIKMUL3BNVVV3IERJPAZXM3PJMDNXYJIZFUL3",
        "GALQ4TZA6VRBBBBYMM3KSBSXJDLC5A7YIGH4SAS6AJ7N4ZA6P6IHWH43",
        "GDMMVCANURBLP6O64QWJM3L2EZTDSGTFL4B2BNXKAQPWYDX6WNAFNWK4",
    ],
}

DATA_ENTRY_KEY = "tft-vesting"
VESTING_SCHEME = "month1=05/2021,48months,priceunlock=tftvalue>month*0.015+0.15"


class VestingService(BaseActor):
    def _get_network(self) -> str:
        return str(get_wallet().network.value)

    def _get_network_passphrase(self) -> str:
        if self._get_network() == "TEST":
            return stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
        return stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE

    def _get_horizon_server(self) -> stellar_sdk.Server:
        return get_wallet()._get_horizon_server()

    def _get_tft_issuer(self) -> str:
        return _TFT_ISSUERS[self._get_network()]

    def _get_cosigners(self) -> list:
        return _COSIGNERS[self._get_network()]

    def _get_cleanup_transaction(self, unlockhash: str):
        data = {"unlockhash": unlockhash}
        resp = j.tools.http.post(
            f"https://{'testnet.threefold.io' if self._get_network()=='TEST' else'tokenservices.threefold.io'}/threefoldfoundation/unlock_service/get_unlockhash_transaction",
            json={"args": data},
        )
        if resp.status_code == j.tools.http.status_codes.codes.NOT_FOUND:
            return None
        resp.raise_for_status()
        return resp.json()["transaction_xdr"]

    def _is_valid_cleanup_transaction(self, vesting_account_id: str, preauth_signer: str) -> bool:

        unlock_tx = self._get_cleanup_transaction(unlockhash=preauth_signer)
        if not unlock_tx:
            return False
        txe = stellar_sdk.TransactionEnvelope.from_xdr(
            unlock_tx,
            stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
            if self._get_network() == "TEST"
            else stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE,
        )
        tx = txe.transaction
        if tx.source.account_id != vesting_account_id:
            return False
        if len(tx.operations) != 3:
            return False
        change_trust_op = tx.operations[0]
        if not type(change_trust_op) is stellar_sdk.ChangeTrust:
            return False
        if not change_trust_op.source is None:
            return False
        if int(change_trust_op.limit) != 0:
            return False
        if change_trust_op.asset.code != "TFT" or change_trust_op.asset.issuer != self._get_tft_issuer():
            return False
        manage_data_op = tx.operations[1]
        if not type(manage_data_op) is stellar_sdk.ManageData:
            return False
        if not manage_data_op.source is None:
            return False
        if manage_data_op.data_name != DATA_ENTRY_KEY:
            return False
        if not manage_data_op.data_value is None:
            return False
        account_merge_op = tx.operations[2]
        if not type(account_merge_op) is stellar_sdk.AccountMerge:
            return False
        if not account_merge_op.source is None:
            return False
        if account_merge_op.destination.account_id != get_wallet().address:
            return False
        return True

    def _verify_signers(self, account_record, owner_address: str) -> bool:
        # verify tresholds
        tresholds = account_record["thresholds"]
        if tresholds["low_threshold"] != 10 or tresholds["med_threshold"] != 10 or tresholds["high_threshold"] != 10:
            return False
        ## signers found for account
        signers = {signer["key"]: (signer["weight"], signer["type"]) for signer in account_record["signers"]}
        # example of signers item --> {'GCWPSLTHDH3OYH226EVCLOG33NOMDEO4KUPZQXTU7AWQNJPQPBGTLAVM':(5,'ed25519_public_key')}

        # Check all cosigners are in account signers with weight 1
        for correct_signer in _COSIGNERS[self._get_network()]:
            if (
                correct_signer in signers.keys()
                and signers[correct_signer][0] == 1
                and signers[correct_signer][1] == "ed25519_public_key"
            ):
                continue
            else:
                return False

        account_id = account_record["account_id"]

        cleanup_signer_correct = False
        master_key_weight_correct = False
        owner_key_weight_correct = False
        for signer in account_record["signers"]:
            if signer["type"] == "preauth_tx":
                if signer["weight"] != 10:
                    return False
                cleanup_signer_correct = self._is_valid_cleanup_transaction(account_id, signer["key"])
                continue
            if signer["type"] != "ed25519_public_key":
                return False
            if signer["key"] == account_id:
                master_key_weight_correct = signer["weight"] == 0
            if signer["key"] == owner_address:
                owner_key_weight_correct = signer["weight"] == 5
        if len(account_record["signers"]) == 12:
            return cleanup_signer_correct and master_key_weight_correct and owner_key_weight_correct
        return len(account_record["signers"]) == 11 and master_key_weight_correct and owner_key_weight_correct

    def _get_vesting_accounts(self, address: str) -> list:
        vestingaccounts = []

        accounts_endpoint = get_wallet()._get_horizon_server().accounts()
        accounts_endpoint.for_signer(address)
        old_cursor = "old"
        new_cursor = ""
        while new_cursor != old_cursor:
            old_cursor = new_cursor
            accounts_endpoint.cursor(new_cursor)
            response = accounts_endpoint.call()
            next_link = response["_links"]["next"]["href"]
            next_link_query = parse.urlsplit(next_link).query
            cursor = parse.parse_qs(next_link_query, keep_blank_values=True).get("cursor")
            new_cursor = cursor[0]
            for record in response["_embedded"]["records"]:
                if "tft-vesting" in record.get("data"):
                    decoded_data = j.data.serializers.base64.decode(record["data"]["tft-vesting"]).decode()
                    if decoded_data == VESTING_SCHEME:
                        if self._verify_signers(record, address):
                            vestingaccounts.append(record)
        return vestingaccounts

    @actor_method
    def vesting_accounts(self, owner_address: str = "") -> dict:
        if owner_address == "":
            raise j.exceptions.Value("owner_address is required")
        try:
            found_vesting_accounts = self._get_vesting_accounts(owner_address)
            vesting_accounts = []
            data = {"owner_adress": owner_address}
            for found_vesting_account in found_vesting_accounts:
                tokenbalances = [
                    b["balance"]
                    for b in found_vesting_account["balances"]
                    if b["asset_type"] == "credit_alphanum4"
                    and b["asset_code"] == "TFT"
                    and b["asset_issuer"] == self._get_tft_issuer()
                ]
                tokenbalance = tokenbalances[0] if tokenbalances else "0"
                vesting_account = {"address": found_vesting_account["account_id"], "TFT": tokenbalance}
                vesting_accounts.append(vesting_account)
            data["vesting_accounts"] = vesting_accounts

        except stellar_sdk.exceptions.NotFoundError as e:
            j.logger.exception("Error: Address not found", exception=e)
            data = {"Error": "Address not found"}

        except stellar_sdk.exceptions.BadRequestError as e:
            if e.extras.get("invalid_field", "") == "account_id":
                data = {"Error": "Address not valid"}
            else:
                data = {"Error": f"{e.title}: {e.detail}"}
            j.logger.exception(str(data), exception=e)

        except j.exceptions.Value as e:
            data = {"Error": e.args[0]}
            j.logger.exception(str(data), exception=e)

        return data

    @actor_method
    def unvestingtransaction(self, vestingaccount: str = "") -> str:
        unvesting_transaction = get_unvesting_transactions().get(vestingaccount, None)
        if not unvesting_transaction:
            raise j.exceptions.NotFound("No unvesting transaction found for this address")
        return unvesting_transaction


Actor = VestingService
