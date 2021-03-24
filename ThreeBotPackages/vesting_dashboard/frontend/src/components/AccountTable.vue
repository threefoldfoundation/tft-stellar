<template>
  <div>
    <v-data-table
      v-if="loading"
      item-key="name"
      class="elevation-1 mt-16"
      loading
      loading-text="Loading... Please wait"
    ></v-data-table>
    <v-data-table
      v-else
      :headers="headers"
      :items="vestinginfo"
      :items-per-page="5"
      class="elevation-1 mt-16"
      item-key="owner"
      show-expand
      :single-expand="singleExpand"
      :expanded.sync="expanded"
    >
      <template slot="no-data">No accounts added</template>

      <template v-slot:item.owner="{ item }">
        <div>{{ item.owner }}</div>
      </template>

      <template v-slot:item.vesting="{ item }">
        <div>{{ item.vesting }}</div>
      </template>

      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length">
          <AccountInfo :key="item.id" :info=item />
        </td>
      </template>
    </v-data-table>

  </div>
</template>

<script>
import AccountInfo from "./AccountInfo"
export default {
  props: ['vestinginfo', 'loading'],
  components: {
    AccountInfo
  },
  data() {
    return {
      headers: [
        { text: "Owner Account Address", value: "owner" },
        { text: "Vesting Account Address", value: "vesting" }
      ],
      expanded: [],
      singleExpand: true
    }
  },
  methods: {
    openAccountDetails (account) {
      const index = this.expanded.indexOf(account)
      if (index > -1) this.expanded.splice(index, 1)
      else this.expanded.push(account)
    }
  },
}
</script>
