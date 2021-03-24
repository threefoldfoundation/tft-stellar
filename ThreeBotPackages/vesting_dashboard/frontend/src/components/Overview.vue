<template>
  <div>
    <VestingForm :getVestingInfo="getVestingInfo" :setLoading="setLoading" />
    <AccountTable :vestinginfo="vestinginfo" :loading="loading" />
  </div>
</template>

<script>
import VestingServices from "../services/VestingServices"
import VestingForm from "./VestingForm"
import AccountTable from "./AccountTable"
export default {
  name: "App",
  components: {
    VestingForm,
    AccountTable,
  },
  mounted () {
    this.getVestingInfo()
  },
  data () {
    return {
      vestinginfo: [],
      loading: false
    }
  },
  methods: {
    getVestingInfo(){
      this.loading = true
      VestingServices.listAccounts()
        .then((response) => {
          this.loading = false
          this.vestinginfo = response.data.data
        })
        .catch((error) => {
          this.loading = false
          console.log("Error! Could not reach the API. " + error)
        })
    },
    setLoading (loading) {
      this.loading = loading
    }
  }
}
</script>