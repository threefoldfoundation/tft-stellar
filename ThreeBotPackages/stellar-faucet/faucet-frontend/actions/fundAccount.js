import axios from 'axios'
import config from '../public/config'

export function fundAccount(destination, username, signed_hash) {
  return axios.post("http://localhost/threefoldfoundation/stellar_faucet/actors/stellar_faucet/transfer", { args: { destination, username, signed_hash } })
}

export function getUserData (doubleName) {
  return axios.get(`${config.botBackend}/api/users/${doubleName}`)
}