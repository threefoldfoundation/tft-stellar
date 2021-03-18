<template>
  <v-app>
    <v-main>
      <v-container class="my-5">
        <v-img
          lazy-src="./assets/3bot_robot.png"
          height="auto"
          width="150"
          src="./assets/3bot_robot.png"
          class="mx-auto mt-5"
        ></v-img>
        <VestingForm class="mb-16" />

        <AccountTable />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import VestingForm from "./components/VestingForm";
import AccountTable from "./components/AccountTable";
export default {
  name: "App",
  components: {
    VestingForm,
    AccountTable,
  },
};
</script>