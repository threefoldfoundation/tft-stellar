# Sponsored reserves testscripts

Use the python virtualenv as described in the [scripts readme](../../scripts/readme.md).

Activating accounts with sponsorship works fine.

Doing an account merge to remove the account gives a stellar `{"transaction":"tx_internal_error"}` error.
This is a known bug: https://github.com/stellar/stellar-core/issues/2914

According to the bug report:
"The workaround for Account Merge is to first transfer sufficient quantity of Lumens to remove sponsorship, revoke sponsorship, then perform Account Merge"

Revoking sponsorship needs to be done by the sponsoring account, it can not be done by the sponsored account.
