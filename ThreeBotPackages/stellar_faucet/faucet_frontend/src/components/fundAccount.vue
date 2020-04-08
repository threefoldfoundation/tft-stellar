<template>
  <v-app id="inspire">
      <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col
            cols="4"
            lg="12"
            md="10"
            sm="6"
          >
            <h1>FreeTFT Faucet</h1>
            <v-card class="elevation-12">
              <v-toolbar
                color="primary"
                dark
                flat
              >
                <v-toolbar-title class="title">Fund a FreeTFT address</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form v-on:submit.prevent="fundAddress">
                  <v-text-field v-model="address" required placeholder="Address" />
                  <p v-if="error" id="errortext">This address probably does not exist or does not have a trustline with the issuer of our Stellar TFT (Testnet).</p>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer />
                <v-btn
                  color="primary"
                  class="ma-2"
                  :loading="loading"
                  :disabled="loading || address === ''"
                  v-on:click="fundAddress()">
                  Fund
                </v-btn>
              </v-card-actions>
            </v-card>
            <br>
            <br>
            <v-card class="elevation-12">
              <v-card-text>
                <p>Here you can request FreeTFT, you can use this FreeTFT to pay for free capacity. Fill in a valid stellar address that has a trustline to the issuer of FreeTFT tokens.</p>
              </v-card-text>
            </v-card>
            
          </v-col>
        </v-row>
      </v-container>
  </v-app>
</template>

<script lang="ts">
/* eslint-disable */
import { fundAccount, getUserData } from "../../actions/fundAccount"
import CryptoService from "../services/CryptoService"

export default {
  data() {
    return {
      error: false,
      address: "",
      loading: false,
      signedAttemptObject: undefined,
      username: undefined
    }
  },
  async mounted() {
    let url = new URL(window.location.href)

    let error = url.searchParams.get('error')

    if (error) {
      console.log('Error: ', error)
      return
    }

    let signedAttemptObject = JSON.parse(url.searchParams.get('signedAttempt'));
    this.signedAttemptObject = signedAttemptObject
  },
  methods: {
    fundAddress() {
      this.loading = true
      this.error = false
      
      console.log(this.signedAttemptObject)
      fundAccount(this.address, this.signedAttemptObject)
        .then(res => {
          if (res.status == 200) {
            this.loading = false
            this.$toasted.success("Address funded successfully")
          } else {
            this.error = true
          }
        })
        .catch(() => {
          this.error = true
          this.loading = false
        })
    }
  },
  name: "FundAccount"
}
</script>
<style scoped>
#errortext {
  color: red;
}
#inspire {
  width: 1200px;
}
h1 {
  font-family: 'Bebas Neue', cursive;
  color: #1072ba
}
p {
  font-family: 'Lato', sans-serif;
}
.title {
  font-family: 'Lato', sans-serif;
}
.logo {
  width: 40px;
  height: 40px;
}
</style>
