import axios from 'axios'

export function fundAccount(destination) {
  return axios.post("http://localhost/threefoldfoundation/stellar_faucet/actors/stellar_faucet/transfer", { args: { destination } })
}
