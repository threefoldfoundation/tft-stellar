<template>
  <v-app>
    <v-main>
      <v-container class="my-5">
        <v-img
          lazy-src="./assets/3fold_logo.png"
          height="auto"
          width="325"
          src="./assets/3fold_logo.png"
          class="mx-auto mt-5"
        ></v-img>
        <Overview class="mb-16" />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import Overview from "./components/Overview"
export default {
  name: "App",
  components: {
    Overview,
  },
};
</script>