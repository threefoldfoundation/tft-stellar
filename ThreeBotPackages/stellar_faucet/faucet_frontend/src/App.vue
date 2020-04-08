<template>
  <v-app>
    <v-img class="logo" :src="require('../public/3logo.png')" />
    <v-content fill-height>
      <v-layout justify-center fill-height>
        <v-layout column align-center justify-center>
          <router-view/>
        </v-layout>
      </v-layout>
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: 'App'
}
</script>
<style scoped>
.logo {
  width: 40px;
  height: 40px;
  margin-left: 50px;
  margin-top: 20px;
}
</style>