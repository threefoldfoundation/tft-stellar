import Vue from 'vue'
import Vuetify from 'vuetify/lib'

Vue.use(Vuetify)


export default new Vuetify({
    theme: {
        dark: false,
        themes: {
            dark: {
                primary: "#57be8e",
            },
            light: {
                primary: "#57be8e",
            }
        }
    },
})
