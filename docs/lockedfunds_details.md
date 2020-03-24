# Technical details of locked funds

In this example, the sender with adddress `GCSYR5OI3W2SC3EVF6PPLHGNBTSKX5L57HIX4BKMQPZJNEHA6ICQ2BJO` sends 100 TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3 (TFT on testnet) to the receiver with address `GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O` which are locked for 1 hour before the receiver can claim them.

## Sending

So the sender creates an escrow account, activates it with at least 2+ 0.5* 4( 1 trustline and the  signers) + basefee*4  XLM.

Now, a trustline from the escrow account to TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3 is created.

An unlocktransaction is made that  modifies the escrow escrow account to require only 1 signer and sets the  weight of the masterkey to 0. This unlocktransaction has timebounds set so it can only be submitted to the Stellar network witin an hour.

The sender adds the receiver and the hash of the unlocktransaction as signers to the escrow account.

The unlocktransaction is now published publicly to the unlock transaction service so the receiver can pick it up to know the timebounds and possibly check if everything is as agreed.

Everything is prepared so it is safe for the sender to transfer 100 TFT to the escrow account.

Now, let's have a look at the created escrow account.

url: `https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A`

```json

{
  "_links": {
    "self": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A"
    },
    "transactions": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/transactions{?cursor,limit,order}",
      "templated": true
    },
    "operations": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/operations{?cursor,limit,order}",
      "templated": true
    },
    "payments": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/payments{?cursor,limit,order}",
      "templated": true
    },
    "effects": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/effects{?cursor,limit,order}",
      "templated": true
    },
    "offers": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/offers{?cursor,limit,order}",
      "templated": true
    },
    "trades": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/trades{?cursor,limit,order}",
      "templated": true
    },
    "data": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/data/{key}",
      "templated": true
    }
  },
  "id": "GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A",
  "account_id": "GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A",
  "sequence": "3486950803636226",
  "subentry_count": 3,
  "last_modified_ledger": 811871,
  "thresholds": {
    "low_threshold": 2,
    "med_threshold": 2,
    "high_threshold": 2
  },
  "flags": {
    "auth_required": false,
    "auth_revocable": false,
    "auth_immutable": false
  },
  "balances": [
    {
      "balance": "100.0000000",
      "limit": "922337203685.4775807",
      "buying_liabilities": "0.0000000",
      "selling_liabilities": "0.0000000",
      "last_modified_ledger": 811872,
      "is_authorized": true,
      "asset_type": "credit_alphanum4",
      "asset_code": "TFT",
      "asset_issuer": "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3"
    },
    {
      "balance": "3.9999600",
      "buying_liabilities": "0.0000000",
      "selling_liabilities": "0.0000000",
      "asset_type": "native"
    }
  ],
  "signers": [
    {
      "weight": 1,
      "key": "GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O",
      "type": "ed25519_public_key"
    },
    {
      "weight": 1,
      "key": "GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A",
      "type": "ed25519_public_key"
    },
    {
      "weight": 1,
      "key": "TBRWRROFJZ7XITHGYCNI2TMVGSATRAUE5LY2KPBV2RIAVMXUDMTA3APV",
      "type": "preauth_tx"
    }
  ],
  "data": {},
  "paging_token": "GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A"
}
```

The escrow account has a balance of 100 TFT, needs at least 2 signatures for all tresholds, the signers contain the receiver and a preauth transaction hash of the unlock transaction.

## Receiving

The receiver has to find the escrow account first. This can be done by listing the accounts for which the receiving address is a signer.

url: `https://horizon-testnet.stellar.org/accounts/?signer=GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O`

```json
{
  "_links": {
    "self": {
      "href": "https://horizon-testnet.stellar.org/accounts/?cursor=&limit=10&order=asc&signer=GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O"
    },
    "next": {
      "href": "https://horizon-testnet.stellar.org/accounts/?cursor=GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A&limit=10&order=asc&signer=GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O"
    },
    "prev": {
      "href": "https://horizon-testnet.stellar.org/accounts/?cursor=GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O&limit=10&order=desc&signer=GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O"
    }
  },
  "_embedded": {
    "records": [
      {
        "_links": {
          "self": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O"
          },
          "transactions": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O/transactions{?cursor,limit,order}",
            "templated": true
          },
          "operations": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O/operations{?cursor,limit,order}",
            "templated": true
          },
          "payments": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O/payments{?cursor,limit,order}",
            "templated": true
          },
          "effects": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O/effects{?cursor,limit,order}",
            "templated": true
          },
          "offers": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O/offers{?cursor,limit,order}",
            "templated": true
          },
          "trades": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O/trades{?cursor,limit,order}",
            "templated": true
          },
          "data": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O/data/{key}",
            "templated": true
          }
        },
        "id": "GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O",
        "account_id": "GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O",
        "sequence": "3486920738865153",
        "subentry_count": 1,
        "last_modified_ledger": 811865,
        "thresholds": {
          "low_threshold": 0,
          "med_threshold": 0,
          "high_threshold": 0
        },
        "flags": {
          "auth_required": false,
          "auth_revocable": false,
          "auth_immutable": false
        },
        "balances": [
          {
            "balance": "0.0000000",
            "limit": "922337203685.4775807",
            "buying_liabilities": "0.0000000",
            "selling_liabilities": "0.0000000",
            "last_modified_ledger": 811865,
            "is_authorized": true,
            "asset_type": "credit_alphanum4",
            "asset_code": "TFT",
            "asset_issuer": "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3"
          },
          {
            "balance": "9999.9999900",
            "buying_liabilities": "0.0000000",
            "selling_liabilities": "0.0000000",
            "asset_type": "native"
          }
        ],
        "signers": [
          {
            "weight": 1,
            "key": "GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O",
            "type": "ed25519_public_key"
          }
        ],
        "data": {},
        "paging_token": "GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O"
      },
      {
        "_links": {
          "self": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A"
          },
          "transactions": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/transactions{?cursor,limit,order}",
            "templated": true
          },
          "operations": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/operations{?cursor,limit,order}",
            "templated": true
          },
          "payments": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/payments{?cursor,limit,order}",
            "templated": true
          },
          "effects": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/effects{?cursor,limit,order}",
            "templated": true
          },
          "offers": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/offers{?cursor,limit,order}",
            "templated": true
          },
          "trades": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/trades{?cursor,limit,order}",
            "templated": true
          },
          "data": {
            "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/data/{key}",
            "templated": true
          }
        },
        "id": "GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A",
        "account_id": "GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A",
        "sequence": "3486950803636226",
        "subentry_count": 3,
        "last_modified_ledger": 811871,
        "thresholds": {
          "low_threshold": 2,
          "med_threshold": 2,
          "high_threshold": 2
        },
        "flags": {
          "auth_required": false,
          "auth_revocable": false,
          "auth_immutable": false
        },
        "balances": [
          {
            "balance": "100.0000000",
            "limit": "922337203685.4775807",
            "buying_liabilities": "0.0000000",
            "selling_liabilities": "0.0000000",
            "last_modified_ledger": 811872,
            "is_authorized": true,
            "asset_type": "credit_alphanum4",
            "asset_code": "TFT",
            "asset_issuer": "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3"
          },
          {
            "balance": "3.9999600",
            "buying_liabilities": "0.0000000",
            "selling_liabilities": "0.0000000",
            "asset_type": "native"
          }
        ],
        "signers": [
          {
            "weight": 1,
            "key": "TBRWRROFJZ7XITHGYCNI2TMVGSATRAUE5LY2KPBV2RIAVMXUDMTA3APV",
            "type": "preauth_tx"
          },
          {
            "weight": 1,
            "key": "GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O",
            "type": "ed25519_public_key"
          },
          {
            "weight": 1,
            "key": "GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A",
            "type": "ed25519_public_key"
          }
        ],
        "data": {},
        "paging_token": "GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A"
      }
    ]
  }
}
```

If the result is the filtered to exclude it's own address, the escrow account is found together it's balanceswith the hash of the unlocktransaction, being `TBRWRROFJZ7XITHGYCNI2TMVGSATRAUE5LY2KPBV2RIAVMXUDMTA3APV` in this case.

Having the hash of the unlocktransaction, the unlock transactionenvelope can be obtained from the [unlocktransaction store service](../ThreeBotPackages/unlock-service/readme.md).

 `curl -H "Content-Type: application/json" -d '{ "args": { "unlockhash": "TBRWRROFJZ7XITHGYCNI2TMVGSATRAUE5LY2KPBV2RIAVMXUDMTA3APV"}}' -XPOST "https://testnet.threefold.io/threefoldfoundation/unlock_service/get_unlockhash_transaction"`

response:
```json
{"unlockhash": "TBRWRROFJZ7XITHGYCNI2TMVGSATRAUE5LY2KPBV2RIAVMXUDMTA3APV", "transaction_xdr": "AAAAAOZagjJNeF2pQReStULsfSDHk6WoYTloVY7NBq8AbbgsAAAAZAAMY10AAAADAAAAAQAAAABedOIYAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAFAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAAAAAAAAAAAAAAAAAABAG24LAAAAEDPghy9Oq3+WYK0wTYnj3gyFwYqRzkDxkBWLdQAG8ykZxY+CMLBpz4tW6/M+ctInZNdVu6dzrajSC4mrlBY5uoM", "id": 1}
```

TODO: [This crashes at the moment](https://github.com/threefoldfoundation/tft-stellar/issues/42).

The service returns the transaction envelope in xdr:

`AAAAAOZagjJNeF2pQReStULsfSDHk6WoYTloVY7NBq8AbbgsAAAAZAAMY10AAAADAAAAAQAAAABedOIYAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAFAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAAAAAAAAAAAAAAAAAABAG24LAAAAEDPghy9Oq3+WYK0wTYnj3gyFwYqRzkDxkBWLdQAG8ykZxY+CMLBpz4tW6/M+ctInZNdVu6dzrajSC4mrlBY5uoM`

Decoded here using stellar laboratory but best to do so using the sdk:

```text
sourceAccount: [publicKeyTypeEd25519]
ed25519: GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A
fee: 100
seqNum: 3486950803636227
timeBounds
minTime: 1584718360
maxTime: 0
memo: [memoNone]
operations: Array[1]
[0]
sourceAccount: none
body: [setOption]
setOptionsOp
inflationDest: none
clearFlags: none
setFlags: none
masterWeight: 0
lowThreshold: 1
medThreshold: 1
highThreshold: 1
homeDomain: none
signer: none
ext: [undefined]
signatures: Array[1] Signatures checked!
[0]
hint: G______________________________________________ANW4C____
signature: z4IcvTqt/lmCtME2J494MhcGKkc5A8ZAVi3UABvMpGcWPgjCwac+LVuvzPnLSJ2TXVbunc62o0guJq5QWObqDA==
```

So the Timebounds can be seen and the fact that the masterweight is set to 0 and the other tresholds to 1 along with a valid signature of the masterkey.

When the mintime has expired, this can be submitted to the Stellar network directly
Let's look at the escrow account after submission:

Url: `https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A`

```json
{
  "_links": {
    "self": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A"
    },
    "transactions": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/transactions{?cursor,limit,order}",
      "templated": true
    },
    "operations": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/operations{?cursor,limit,order}",
      "templated": true
    },
    "payments": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/payments{?cursor,limit,order}",
      "templated": true
    },
    "effects": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/effects{?cursor,limit,order}",
      "templated": true
    },
    "offers": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/offers{?cursor,limit,order}",
      "templated": true
    },
    "trades": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/trades{?cursor,limit,order}",
      "templated": true
    },
    "data": {
      "href": "https://horizon-testnet.stellar.org/accounts/GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A/data/{key}",
      "templated": true
    }
  },
  "id": "GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A",
  "account_id": "GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A",
  "sequence": "3486950803636227",
  "subentry_count": 2,
  "last_modified_ledger": 813012,
  "thresholds": {
    "low_threshold": 1,
    "med_threshold": 1,
    "high_threshold": 1
  },
  "flags": {
    "auth_required": false,
    "auth_revocable": false,
    "auth_immutable": false
  },
  "balances": [
    {
      "balance": "100.0000000",
      "limit": "922337203685.4775807",
      "buying_liabilities": "0.0000000",
      "selling_liabilities": "0.0000000",
      "last_modified_ledger": 811872,
      "is_authorized": true,
      "asset_type": "credit_alphanum4",
      "asset_code": "TFT",
      "asset_issuer": "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3"
    },
    {
      "balance": "3.9999500",
      "buying_liabilities": "0.0000000",
      "selling_liabilities": "0.0000000",
      "asset_type": "native"
    }
  ],
  "signers": [
    {
      "weight": 1,
      "key": "GDA5TMZM2WXZZP4BL4ZKEORZI26SBZN5RVQIU664ULBC7KR4J3NFLX2O",
      "type": "ed25519_public_key"
    },
    {
      "weight": 0,
      "key": "GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A",
      "type": "ed25519_public_key"
    }
  ],
  "data": {},
  "paging_token": "GDTFVARSJV4F3KKBC6JLKQXMPUQMPE5FVBQTS2CVR3GQNLYANW4CZ26A"
}
```

This leaves the escrow account in full control of only the receiver.
To Transfer all funds to it's own address, the receiver needs to transfer the TFTand to recover the XLM,  delete the trustline and merge the escrow account o it's own.
