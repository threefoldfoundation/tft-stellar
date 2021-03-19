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
        <v-dialog v-model="dialog" width="700">
            
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                    color="blue lighten-2"
                    dark
                    v-bind="attrs"
                    v-on="on"
                >
                Check transactions
                </v-btn>
            </template>

            <v-card>
                <v-card-title class="headline">Transactions</v-card-title>
                
                <v-card-subtitle>for {{info.vesting}}</v-card-subtitle>
                
                <v-card-text class="pa-1">
                    <p v-if="info.transactions.length === 0">No transactions yet!</p>
                    <ul v-else>
                        <li v-for="tx in info.transactions" :key="tx.transaction_hash">
                            hash: {{tx.transaction_hash}} for {{tx.amount}} TFT's @{{tx.timestamp}} 
                        </li>
                    </ul>
                    <slot name="default"></slot>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <slot name="actions"></slot>
                </v-card-actions>
            </v-card>

        </v-dialog>

      </v-row>
    <v-container />
  </v-col>
</template>

<script>
import VueQrcode from 'vue-qrcode'
export default {
  props: ['info'],
  components: {
    VueQrcode
  },
  data() {
    return {
      escrow: '',
      dialog: false,
    }
  },
  mounted () {
    console.log(this.info.transactions)
  },
  computed: {
    qrCodeValue () {
        return `TFT:${this.info.vesting}`
    }
  }
}
</script>
