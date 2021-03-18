# Vesting UI

The [Vesting spec](./vesting.md) desribes how vesting accounts are set up. The [vesting service](../../ThreeBotPackages/vesting_service) implements a service that creates vesting accounts.

The problem is that wallets do not support this setup and even importing or viewing multisig wallets where you are the signer is not possible in most Stellar wallets like Solar for example.

## Vesting dashboard

A webpage that requires a threefold connect login where a user can

- Create escrow accounts
- View created vesting accounts

### Creating escrow accounts

The user needs to provide the owner address. The vesting service is then called to create a vesting account.

The owner address and the address of the vesting account are stored for the authententicated user.

## View created vesting accounts

List the owner addresses and associated vesting accounts stored at the vesting account creation for the authenticated user.

When going to the detail of the vesting account, the amount of TFT is shown and when it was deposited.

Also a link to stellar.expert should be present where users can view the details of the vesting account and verify themselves that the vesting account is what we say it is if they want to.

Later, an overview of the locked and free TFT's will be added.

>> [User stories on Vesting UI](https://github.com/threefoldfoundation/tft-stellar/blob/master/specs/vesting/vesting_dashboard_userstories.md)
