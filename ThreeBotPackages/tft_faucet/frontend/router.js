import Vue from 'vue'
import Router from 'vue-router'
import fundAccount from './components/fundAccount'

Vue.use(Router)

export default new Router({
  base: "/tft_faucet",
  routes: [
    {
      path: '/fundAccount',
      name: 'fundAccount',
      component: fundAccount
    }
  ]
})
