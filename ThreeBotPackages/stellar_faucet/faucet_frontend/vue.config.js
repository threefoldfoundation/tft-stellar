const path = require("path");
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin')

module.exports = {
  outputDir: path.resolve(__dirname, "../frontend"),
  publicPath: '/',
  configureWebpack: {
    plugins: [
      new VuetifyLoaderPlugin()
    ],
  },
}
