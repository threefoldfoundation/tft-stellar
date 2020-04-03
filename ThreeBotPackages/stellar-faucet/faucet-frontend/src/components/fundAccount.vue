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
import { fundAccount } from "../../actions/fundAccount"
export default {
  data() {
    return {
      error: false,
      address: "",
      loading: false
    }
  },
  methods: {
    fundAddress() {
      this.loading = true
      this.error = false
      var url = new URL(window.location.href)
      const username = url.searchParams.get('username')
      fundAccount(this.address, username)
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
