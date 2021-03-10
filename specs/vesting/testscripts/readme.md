# Vesting testscripts

Use the python virtualenv as described in the [scripts readme](../../scripts/readme.md).

First create the cosigner accounts

```sh
./createcosigners.py
```

Optionally create an account that holds the tokens that are going to be vested

```sh
./createaccount.py
```

Use the secret of the account creation output to add a trustline

```sh
./addtrustline Sxxxx [--fullassetcode=CODE:Issuer]
```

Create an account to fund the escrow account accounts with XLM:

```sh
./createaccount.py
```

Create escrow accounts using `createescrowaccount.py` scrip, passing the  the activationaccount secret and the owner account address as parameters.
