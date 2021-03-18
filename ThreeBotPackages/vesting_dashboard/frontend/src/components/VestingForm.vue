
<template>
  <v-form ref="form" v-model="valid" lazy-validation @submit.prevent="submit">
    <v-row>
      <v-col sm="12">
        <v-text-field
          label="Address"
          :rules="addressRules"
          v-model="address"
          :loading="loading"
        ></v-text-field>
        <v-btn class="primary" type="submit" @click="validate">
          create vesting account
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>

<script>
import VestingServices from "../services/VestingServices";

export default {
  name: "VestingForm",
  data() {
    return {
      loading: false,
      valid: true,
      address: null,
      addressRules: [(v) => !!v || "Address is required"],
    };
  },
  methods: {
    submit() {
      VestingServices.createAccount(this.address)
        .then((response) => {
          console.log(response);
          this.$router.go(0);
        })
        .catch((error) => {
          console.log("Error! Could not reach the API. " + error);
        });
    },
    validate() {
      this.$refs.form.validate();
    },
  },
};
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