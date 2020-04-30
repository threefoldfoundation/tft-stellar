# How to test the conversion service code in JSX

## Prerequisites

- Tfchain address, can be created through the cli or the desktop wallet
    - ensure this address has some balance in TFT
    - create some locked token transfers using the desktop wallet
- Stellar address with trustlines to TFT and TFTA

## Flow

Comment out lines 80-81, 92-93, 96-102 in `./actors/conversion_service.py`

The reason we comment this out is to skip folowing steps for easy testing:

- convert rivine address to stellar address
- lock tfchain address

### Start the Threebot server with these lines commented out.

- Import the converter wallet in JSX
- Create a stellar account in JSX with trustlines to TFT and TFTA

```
p.threefoldfoundation.conversion_service.actors.conversion_service.migrate_tokens(stellar_address=stellarclient.address, tfchain_address="tfchainaddress") 
```

This result should be an array of `unlock_tx_xdrs`