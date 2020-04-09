import Vue from 'vue'
import App from './App.vue'
import vuetify from '../plugins/vuetify' // path to vuetify export
import Toasted from 'vue-toasted'
import router from './router'

Vue.config.productionTip = false

Vue.use(Toasted, { duration: 3000, theme: 'bubble', position: 'bottom-center' })

new Vue({
  vuetify,
  router,
  render: h => h(App),
}).$mount('#app')
