import 'vue-multiselect/dist/vue-multiselect.min.css'
import './assets/scss/main.scss'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)

app.mount('#app')
