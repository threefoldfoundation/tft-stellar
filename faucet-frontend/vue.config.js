const path = require("path");
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin')

module.exports = {
  devServer: {
    host: '0.0.0.0',
    port: '8080',
    public: '0.0.0.0:8080',
    disableHostCheck: true,
  },
  outputDir: path.resolve(__dirname, "../frontend"),
  publicPath: '',
  configureWebpack: {
    plugins: [
      new VuetifyLoaderPlugin()
    ],
  },
}
