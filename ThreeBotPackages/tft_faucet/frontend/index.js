
Vue.use(Vuex)
Vue.use(Vuetify)
// Vue.use(VueRouter)

const vuetify = new Vuetify({
  icons: {
    iconfont: 'mdi'
  },
  theme: {
    themes: {
      dark: {
        navbar: '#363636'
      },
      light: {
        primary: '#1B4F72',
        navbar: '#1B4F72',
        secondary: '#CCCBCA',
        accent: '#59B88C',
        success: "#17A589",
        error: '#EC7063',
      }
    },
  }
})

const fundAccount = httpVueLoader('./components/fundAccount.vue')
const router = new VueRouter({
  base: "/tft_faucet",
  routes: [
    {
      path: '/',
      name: 'fundAccount',
      component: fundAccount
    }
  ]
})


Vue.use(Toasted, { duration: 3000, theme: 'bubble', position: 'bottom-center' })

Vue.prototype.$api = apiClient


const app = httpVueLoader('./App.vue')

new Vue({
  el: '#app',
  components: { App: app },
  vuetify,
  router
})
