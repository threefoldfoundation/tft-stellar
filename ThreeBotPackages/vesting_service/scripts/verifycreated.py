#!/usr/bin/env python
# pylint: disable=no-value-for-parameter
import click
import stellar_sdk
from urllib import parse


def get_owner_address(horizon_server, vesting_account_id: str) -> str:
    accounts_endpoint = horizon_server.accounts().account_id(vesting_account_id)
    response = accounts_endpoint.call()
    owner_signers = [signer for signer in response["signers"] if signer["weight"] == 5]
    return owner_signers[0]["key"] if len(owner_signers) > 0 else None


@click.command(help="Verification of the vesting service")
@click.option("--activationaccount", type=str, default="GB2P3V4GZNYTI3E5IOQHAF2E46GKMW26RHVTD4TZEZAELKLJHUYPH4FR")
@click.option("--network", type=click.Choice(["test", "public"], case_sensitive=False), default="public")
def verify(activationaccount, network):
    horizon_server = stellar_sdk.Server(
        "https://horizon-testnet.stellar.org" if network == "test" else "https://horizon.stellar.org"
    )
    accounts_endpoint = horizon_server.operations().for_account(activationaccount)
    accounts_endpoint.limit(50)
    old_cursor = "old"
    new_cursor = ""

    number_of_vesting_accounts = 0
    vesting_accounts = {}
    invalid_vesting_accounts = []
    while new_cursor != old_cursor:
        old_cursor = new_cursor
        accounts_endpoint.cursor(new_cursor)
        response = accounts_endpoint.call()
        next_link = response["_links"]["next"]["href"]
        next_link_query = parse.urlsplit(next_link).query
        new_cursor = parse.parse_qs(next_link_query, keep_blank_values=True)["cursor"][0]
        for operation in response["_embedded"]["records"]:
            if operation["type"] != "create_account" or operation["source_account"] != activationaccount:
                continue
            vesting_account_id = operation["account"]
            owner_account_id = get_owner_address(horizon_server, vesting_account_id)
            if not owner_account_id:
                invalid_vesting_accounts.append(vesting_account_id)
                continue
            print(f"Created vesting account {vesting_account_id} for owner {owner_account_id}")
            number_of_vesting_accounts += 1
            accounts_for_owner = vesting_accounts.get(owner_account_id, [])
            accounts_for_owner.append(vesting_account_id)
            vesting_accounts[owner_account_id] = accounts_for_owner
    print(
        f"{number_of_vesting_accounts} vesting accounts have been created for {len(vesting_accounts.keys())} owner accounts"
    )
    if len(invalid_vesting_accounts) > 0:
        print("Invalid vesting accounts:")
        print("\n".join(invalid_vesting_accounts))


if __name__ == "__main__":
    verify()
