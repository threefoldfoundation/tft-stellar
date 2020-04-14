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
            cols="3"
            sm="4"
            md="6"
            lg="12"
          >
            <v-img class="logo" :src="require('../../public/faucet-logo.png')" />
            <div class="header">
              <h1>Get FreeTFT's</h1>
            </div>
            <div class="content">
              <div class="">
                <v-text-field v-model="address" label="Enter Stellar address here" :rules="rules" hide-details="auto"></v-text-field>
                <p v-if="error" id="errortext">This address probably does not exist or does not have a trustline with the issuer of our Stellar FreeTFT. Or this address might already have requested tokens before!</p>
              </div>
              <br>
              <br>
              <p>Enter a valid Stellar address to receive FreeTFT, this address must have a trustline to the FreeTFT issuer! You will only be able to receive tokens once.</p>
              <br>
              <br>
              <v-btn
                outlined
                color="#333333"
                class="ma-2"
                :loading="loading"
                :disabled="loading || address === ''"
                v-on:click="fundAddress()">
                Receive your FreeTFT
              </v-btn>
            </div>
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
  },
  methods: {
    fundAddress() {
      this.loading = true
      this.error = false

      let url = new URL(window.location.href)
      const search = url.hash.split("?")[1]
      let params = new URLSearchParams(search);
      const obj = params.get("signedAttempt");
      const signedAttemptObject = JSON.parse(obj)
      fundAccount(this.address, signedAttemptObject)
        .then(res => {
          if (res.status == 200) {
            this.loading = false
            this.$toasted.success("Address funded successfully")
          } else {
            this.error = true
          }
        })
        .catch(err => {
          console.log(err.meta)
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
  color: #333333;
  font-size: 100px;
}	
p {	
  font-family: 'Lato', sans-serif;	
}	
.title {	
  font-family: 'Lato', sans-serif;	
}	

.header {
  margin: auto;
  width: 50%;
  height: 50%;
  text-align: center;
}

.content {
  margin: auto;
  width: 43%;
  height: 80%;
  text-align: center;
}

.logo {
  width: 30%;
  height: 30%;
  margin: auto;
}

@media screen and (max-width: 400px) {
  .logo {
    width: 60%;
    height: 60%;
    margin: auto;
  }
  .content {
    margin: auto;
    width: 80%;
    height: 80%;
    text-align: center;
  }
  h1 {
    font-size: 50px;
  }
}

@media screen and (max-width: 800px) {
  .logo {
    width: 60%;
    height: 60%;
    margin: auto;
  }
  .content {
    margin: auto;
    width: 80%;
    height: 80%;
    text-align: center;
  }
  h1 {
    font-size: 50px;
  }
}
</style>