<script>
import config from '../../public/config.js'
import CryptoService from '../services/CryptoService'
var randomstring = require('randomstring')
export default {
  name: 'login',
  data () {
    return {
      privateKey: null,
      publicKey: null,
      privateKey2: null,
      publicKey2: null,
      message: null,
      encrypted: null,
      decrypted: null,
      nonce: null
    }
  },
  mounted () {
    this.login()
  },
  methods: {
    async login () {
      var state = randomstring.generate()
      window.localStorage.setItem('state', state)
      var keys = await CryptoService.generateKeys(config.seedPhrase)
      var appid = config.appId

      window.location.href = `${config.botFrontEnd}?state=${state}&appid=${appid}&publickey=${encodeURIComponent(CryptoService.getEdPkInCurve(keys.publicKey))}&redirecturl=${encodeURIComponent(config.redirect_url)}`
    },
    async redirect (state, scope, appid, publicKey, redirectUrl) {
      window.location.href = `${config.botFrontEnd}?state=${state}&scope=${scope}&appid=${appid}&publickey=${encodeURIComponent(CryptoService.getEdPkInCurve(publicKey))}&redirecturl=${encodeURIComponent(redirectUrl)}`
    }
  }
}
</script>