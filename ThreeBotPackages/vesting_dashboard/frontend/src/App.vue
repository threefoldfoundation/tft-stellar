<template>
  <v-app>
    <v-main>
      <v-container class="my-5">
        <h2>TFT Vesting Portal</h2>
        <v-img
          lazy-src="./assets/3fold_logo.png"
          height="auto"
          width="250"
          src="./assets/3fold_logo.png"
          class="mx-auto mb-12 mt-12"
        ></v-img>
        <Overview class="mb-16" />
        <h3>© 2021 <a href="https://new.threefold.io" target="blank">ThreeFold Foundation</a>. All rights reserved.</h3>
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
<style scoped>
.my-5 h2 {
  font-size: 40px;
  text-align: center;
}
.my-5 h3 {
  text-align: center;
}
</style>