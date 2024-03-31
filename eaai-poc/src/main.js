import './assets/main.css'
import Vue from 'vue'
import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { BootstrapVue, IconsPlugin, BVToastPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import Home from './views/Home.vue'
import Cook from './views/Cook.vue'
import Plan from './views/Plan.vue'
import User from './views/User.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'home', component: Home },
        { path: '/cook', name: 'cook', component: Cook },
        { path: '/plan', name: 'plan', component: Plan },
        { path: '/user', name: 'user', component: User }
    ]
})

const app = createApp(App)

app.use(router)
Vue.use(BVToastPlugin)
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

app.mount('#app')
