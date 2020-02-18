import Vue from 'vue'
import Vuetify, { colors } from 'vuetify/lib'

Vue.use(Vuetify)


export default new Vuetify({
    theme: {
        dark: true,
        themes: {
            dark: {
                primary: colors.purple.accent4,
            }
        }
    },
})
