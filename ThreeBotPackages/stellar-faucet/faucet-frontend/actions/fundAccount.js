import axios from 'axios'
import config from '../public/config'

export function fundAccount(destination, signedAttemptObject) {
  return axios.post("http://localhost/threefoldfoundation/stellar_faucet/actors/stellar_faucet/transfer", { args: { destination, signedAttemptObject } })
}

export function getUserData (doubleName) {
  return axios.get(`${config.botBackend}/api/users/${doubleName}`)
}