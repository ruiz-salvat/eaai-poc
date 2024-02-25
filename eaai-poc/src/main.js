import './assets/main.css'
import Vue from 'vue'
import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import Home from './views/Home.vue'
import Scan from './views/Scan.vue'
import Cook from './views/Cook.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'home', component: Home },
        { path: '/scan', name: 'scan', component: Scan },
        { path: '/cook', name: 'cook', component: Cook }
    ]
})

const app = createApp(App)

app.use(router)
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

app.mount('#app')
