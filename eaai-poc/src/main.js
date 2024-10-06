import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import VueCookies from 'vue-cookies'
import './scss/styles.scss'
import * as bootstrap from 'bootstrap'
import Landing from './views/Landing.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Home from './views/Home.vue'
import Cook from './views/Cook.vue'
import Plan from './views/Plan.vue'
import User from './views/User.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'landing', component: Landing },
        { path: '/login', name: 'login', component: Login },
        { path: '/register', name: 'register', component: Register },
        { path: '/home', name: 'home', component: Home },
        { path: '/cook', name: 'cook', component: Cook },
        { path: '/plan', name: 'plan', component: Plan },
        { path: '/user', name: 'user', component: User }
    ]
})

const app = createApp(App)

app.use(router)
app.use(VueCookies)

app.mount('#app')