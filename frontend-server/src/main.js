import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import auth from './auth'
import './registerServiceWorker'
import '../src/assets/style.css'

axios.defaults.baseURL='http://127.0.0.1:5000/'
axios.defaults.headers.common['Content-Type']='application/json'
axios.defaults.headers.common['Access-Control-Allow-Origin']='http://127.0.0.1:5000'
axios.interceptors.request.use(config => {
    config.headers["Authentication-Token"] = auth.getToken()
    return config
})
createApp(App).use(store).use(router).mount('#app')
