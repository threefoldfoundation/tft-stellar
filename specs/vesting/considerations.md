# Considerations

## Libp2p

**TODO:** explain why libp2p is a very good option to communicate between the cosigners:

- Zero config
- NAT traversal + peer routing

## Posting the unvesting transaction from the wallet to the cosigners

The wallet is running in a browser, ideally it would post it's prepared transaction immediately to the cosigners. We use libp2p for communication with the cosigners but browser js libp2p has some limitations:

- Only the websockets transport is supported
- Peer routing is in prototype phase
- Bootstrap discovery in in the "in progress" phase

## Coordinating the signing from the Python vesting service implementation

Libp2p is very immature and incompatible with implementations in other langusges.
