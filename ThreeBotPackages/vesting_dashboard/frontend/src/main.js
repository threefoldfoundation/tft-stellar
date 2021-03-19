import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import Toasted from 'vue-toasted'

Vue.config.productionTip = false

Vue.use(Toasted)

new Vue({
    vuetify,
    render: h => h(App)
}).$mount('#app')