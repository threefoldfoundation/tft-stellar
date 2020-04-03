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
            cols="10"
            sm="12"
            md="6"
          >
            <h1>Stellar Faucet</h1>
            <v-card class="elevation-12">
              <v-toolbar
                color="primary"
                dark
                flat
              >
                <v-toolbar-title>Fund a Stellar address</v-toolbar-title>
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
      verifiedSignedAttempt: undefined,
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

    let user = signedAttemptObject['doubleName']
    this.username = user
    let userPublicKey = (await getUserData(user)).data.publicKey

    let verifiedSignedAttempt

    try {

      var utf8ArrayToStr = (function () {
        var charCache = new Array(128)
        var charFromCodePt = String.fromCodePoint || String.fromCharCode
        var result = []

        return function (array) {
          var codePt, byte1
          var buffLen = array.length

          result.length = 0

          for (var i = 0; i < buffLen;) {
            byte1 = array[i++]

            if (byte1 <= 0x7F) {
              codePt = byte1
            } else if (byte1 <= 0xDF) {
              codePt = ((byte1 & 0x1F) << 6) | (array[i++] & 0x3F)
            } else if (byte1 <= 0xEF) {
              codePt = ((byte1 & 0x0F) << 12) | ((array[i++] & 0x3F) << 6) | (array[i++] & 0x3F)
            } else if (String.fromCodePoint) {
              codePt = ((byte1 & 0x07) << 18) | ((array[i++] & 0x3F) << 12) | ((array[i++] & 0x3F) << 6) | (array[i++] & 0x3F)
            } else {
              codePt = 63
              i += 3
            }

            result.push(charCache[codePt] || (charCache[codePt] = charFromCodePt(codePt)))
          }

          return result.join('')
        }
      })()

      verifiedSignedAttempt = JSON.parse(utf8ArrayToStr(await CryptoService.validateSignedAttempt(signedAttemptObject['signedAttempt'], userPublicKey)))

      if (!verifiedSignedAttempt) {

        console.log('The signedAttempt could not be verified.')
        return
      }

      let state = window.localStorage.getItem('state')

      if (verifiedSignedAttempt['signedState'] !== state) {

        console.log('The state cannot be matched.')
        return
      }

      if (verifiedSignedAttempt['doubleName'] !== user) {

        console.log('The name cannot be matched.')
        return
      }

      this.verifiedSignedAttempt = verifiedSignedAttempt
    } catch (e) {
      console.log('The signedAttempt could not be verified.')
      return
    }
  },
  methods: {
    fundAddress() {
      this.loading = true
      this.error = false
      
      console.log(this.verifiedSignedAttempt)
      fundAccount(this.address, this.username, this.verifiedSignedAttempt.signedState)
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
</style>
