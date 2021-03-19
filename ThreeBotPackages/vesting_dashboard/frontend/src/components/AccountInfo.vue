<template>
  <v-col>
    <div class="title">
      Account Information
    </div>
    <v-container fluid>
      <v-row>
        <v-flex xs3 class="text-left pr-2">Owner </v-flex>
        <v-flex class="text-truncate font-weight-bold">
          <span>{{info.owner}}</span>
        </v-flex>
      </v-row>

      <v-row>
        <v-flex xs3 class="text-left pr-2">Vesting account ID </v-flex>
        <v-flex class="text-truncate font-weight-bold">
          <span>{{info.vesting}}</span>
        </v-flex>
      </v-row>

      <v-row :key="balance.balance" v-for="balance in info.balances">
        <v-flex xs3 class="text-left pr-2 text-truncate" >{{ balance.asset }} </v-flex>
        <v-flex class="text-truncate font-weight-bold">
            <span>{{balance.balance}}</span>
        </v-flex>
      </v-row>

      <v-row>
        <v-flex xs3 class="text-left pr-2">Deposit funds</v-flex>        
      </v-row>

      <v-row>
        <v-flex xs3 class="text-left pr-2">
            <VueQrcode :value="qrCodeValue"/>
        </v-flex>
      </v-row>

      <v-row>
        <v-icon
          small
          class="mr-2"
          @click.stop="viewTransactions(info.transactions, info.vesting)"
        >
          mdi-information-outline
        </v-icon>
      </v-row>
      <Dialog :show="show" :escrow="escrow" :transactions="transactions" />
    <v-container />
  </v-col>
</template>

<script>
import Dialog from "./Dialog"
import VueQrcode from 'vue-qrcode'
export default {
  props: ['info'],
  components: {
    VueQrcode,
    Dialog
  },
  data() {
    return {
      transactions: [],
      escrow: undefined,
      show: false,
    }
  },
  computed: {
    qrCodeValue () {
        return `TFT:${this.info.vesting}`
    }
  },
  methods: {
    viewTransactions(transactions, escrow){
      this.transactions = transactions
      this.escrow = escrow
      this.show = true
    },
  },
}
</script>
