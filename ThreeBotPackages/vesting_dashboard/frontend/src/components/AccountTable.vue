<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="vestinginfo"
      :items-per-page="5"
      v-if="vestinginfo"
      class="elevation-1 mt-16"
      @click:row="handleClick()"
    >
      <template slot="no-data">No accounts added</template>
        <template v-slot:item.owner="{ item }">
          <div>{{ item.owner }}</div>
        </template>

        <template v-slot:item.vesting="{ item }">
          <div>{{ item.vesting }}</div>
        </template>


        <template v-slot:item.transactions="{ item }">
          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon @click.stop="viewTransactions(item.transactions)">
                <v-icon v-bind="attrs" v-on="on" color="#810000"
                  >mdi-information-outline</v-icon
                >
              </v-btn>
            </template>
            <span>Transactions</span>
          </v-tooltip>
      </template>
    </v-data-table>

    <Dialog v-if="selected" v-model="info" :data="selected" />
  </div>
</template>

<script>
import Dialog from "./Dialog";
import VestingServices from "../services/VestingServices";
export default {
  components: {
    Dialog,
  },
  data() {
    return {
      selected: null,
      info: false,
      vestinginfo: null,
      headers: [
        { text: "Owner", value: "owner" },
        { text: "Vesting", value: "vesting" },
        { text: "Transactions", value: "transactions" },
      ]
    };
  },
  computed: {
    vestings() {
      if (!this.vestinginfo) {
        this.getVestingInfo();
      }
      return this.vestinginfo;
    },
  },
  methods: {
    handleClick(account) {
      this.selected = account;
      this.info = true;
      console.log(account);
    },
    viewTransactions(transactions){
      console.log(transactions);
    },
    getVestingInfo(){
      VestingServices.listAccounts()
      .then((response) => {
        console.log(response.data.data);
        this.vestinginfo = response.data.data;
      })
      .catch((error) => {
        console.log("Error! Could not reach the API. " + error);
      });
    }
  },
  mounted() {
    this.getVestingInfo();
  },

};
</script>
