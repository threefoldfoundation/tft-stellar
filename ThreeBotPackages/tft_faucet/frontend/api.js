// const axios = require('axios')

const apiClient = {
  fundAccount: (destination) => {
    return axios({
      url: `/tft_faucet/api/transfer`,
      headers: { 'Content-Type': 'application/json' },
      data: { "destination": destination },
      method: "post"
    })
  }

}

