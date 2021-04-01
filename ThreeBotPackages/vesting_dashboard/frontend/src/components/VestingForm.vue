
<template>
  <v-form ref="form" v-model="valid" lazy-validation @submit.prevent="submit">
    <v-row>
      <v-col sm="12">
        <v-text-field
          label="Insert your TFT Wallet Address"
          :rules="addressRules"
          v-model="address"
          :loading="loading"
        ></v-text-field>
        <v-btn class="primary" type="submit" @click="validate">
          create vesting account
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <span>The vested tokens will be returned to your wallet according to these <a target="blank" href="https://github.com/threefoldfoundation/info_foundation_archive/blob/development/src/token/vesting_pool.md">specifications</a></span>
      </v-col>
    </v-row>
  </v-form>
</template>

<script>
import VestingServices from "../services/VestingServices"

export default {
  props: ['getVestingInfo', 'setLoading'],
  name: "VestingForm",
  data() {
    return {
      loading: false,
      valid: true,
      address: null,
      addressRules: [(v) => !!v || "Address is required"],
    }
  },
  methods: {
    submit() {
      this.setLoading(true)
      VestingServices.createAccount(this.address)
        .then(() => {
          this.$toasted.show('Created vesting account!', { type: 'success', duration: 5000 })
          this.getVestingInfo()
        })
        .catch((error) => {
          this.setLoading(false)
          console.log(error.response)
          let message = error.response.data
          this.$toasted.show(message, { type: 'error', duration: 5000 })
        })
    },
    validate() {
      this.$refs.form.validate()
    },
  },
}
</script>

<style scoped>
.v-form {
  text-align: center;
}
.v-input {
  display: inline-flex;
  width: 50%;
  margin-right: 20px;
  padding-top: 0;
}

.v-application .primary {
  background-color: #399e97 !important;
}
</style>