import { defineConfig } from '@vue/cli-service'
export default defineConfig({
  transpileDependencies: true,
  devServer: {
    host: '127.0.0.1',
    port: 8080,
  },
  productionSourceMap: false,
  configureWebpack: {
    optimization: {
      minimize: false,
    },
  },
  pwa: {
    name: 'Paper Basket',
    shortName: 'paper_basket',
    themeColor: '#fcc03f',
    backgroundColor:'#ffffff',
    msTileColor: '#fcc03f',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: 'black',
    icons: [
      {
        src: 'img/icons/favicon-32x32.png',
        sizes: '32x32',
        type: 'image/png',
        purpose: 'any maskable',
      },
      {
        src: 'img/icons/favicon-16x16.png',
        sizes: '16x16',
        type: 'image/png',
        purpose: 'any maskable',
      },
      {
        src: 'img/icons/apple-touch-icon-152x152.png',
        sizes: '152x152',
        type: 'image/png',
      },
      {
        src: 'img/icons/safari-pinned-tab.svg',
        color: '#5bbad5',
      },
      {
        src: 'img/icons/msapplication-icon-144x144.png',
        sizes: '144x144',
        type: 'image/png',
      },
    ],
    manifestOptions: {
      start_url: '/',
      display:'standalone',
      orientation:'portrait',
      background_color: '#ffffff',
      description: '"Paper Basket" is your one-stop solution for hassle-free grocery shopping. Say goodbye to the long queues and tedious checkouts! With our progressive web app, you can browse, select, and purchase your groceries with ease, all from the comfort of your home.'
    },
    workboxPluginMode: 'InjectManifest',
    workboxOptions: {
      swSrc: './src/service-worker.js'
    }
  }
})
