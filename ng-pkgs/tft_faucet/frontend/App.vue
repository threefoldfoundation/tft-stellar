<template>
  <v-app id="inspire">
    <div>
      <v-img class="logo" src="./assets/3logo.png" />
    </div>
    <v-main fill-height>
      <!-- <v-layout justify-center fill-height>
      <v-layout column align-center justify-center>-->
      <router-view />
      <!-- </v-layout>
      </v-layout>-->
    </v-main>
  </v-app>
</template>


<style scoped>
.logo {
  width: 40px;
  height: 40px;
  margin-left: 50px;
  margin-top: 20px;
}
</style>