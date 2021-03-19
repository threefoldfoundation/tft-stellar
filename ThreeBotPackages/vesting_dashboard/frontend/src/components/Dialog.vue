<template>
  <v-dialog v-model="show" width="700">
    <v-card :loading="loading" :disabled="loading">
      <v-card-title class="headline">Transactions</v-card-title>
      <v-card-subtitle>for {{escrow}}</v-card-subtitle>
      <v-card-text class="pa-5">
        <v-alert v-if="error" dense outlined type="error" class="mb-5">
          {{ error }}
        </v-alert>

        <p v-if="transactions.length === 0">No transactions yet!</p>
        <ul v-else>
          <li v-for="tx in transactions" :key="tx.transaction_hash">
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
</template>

<script>
export default {
  name: "Dialog",
  props: ['show', 'escrow', 'transactions']
};
</script>