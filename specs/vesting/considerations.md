# Considerations

## Libp2p

- Zero config

  Since a Stellar address is just a ED25119 public key, we can use decentralized communication and peerdiscovery if the peers are discoverable through a derivative of this public key. [Libp2p](https://libp2p.io) is such a communication system.

- NAT traversal + peer routing

## Posting the unvesting transaction from the wallet to the cosigners

The wallet is running in a browser, ideally it would post it's prepared transaction immediately to the cosigners. We use libp2p for communication with the cosigners but browser js libp2p has some limitations:

- Only the websockets transport is supported
- Peer routing is in prototype phase
- Bootstrap discovery in in the "in progress" phase

## Coordinating the signing from the Python vesting service implementation

Libp2p is very immature and incompatible with implementations in other langusges.
