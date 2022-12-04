import {createRouter, createWebHashHistory} from "vue-router"
import RegisterView from "@/views/RegisterView"
import LoginView from "@/views/LoginView"
import BoardView from "@/views/BoardView"

import store from "@/store";

const routes = [
    {
        path: '/register',
        name: 'register',
        meta: {
            title: 'Register'
        },
        component: RegisterView
    },
    {
        path: '/login',
        name: 'login',
        meta: {
            title: 'Login'
        },
        component: LoginView
    },
    {
        path: '/',
        name: 'board',
        meta: {
            title: 'Board'
        },
        component: BoardView,
    },
    {
        path: '/summary',
        name: 'summary',
        meta: {
            title: 'Summary'
        },
        component: () => import(/* webpackChunkName: "summary" */ '@/views/SummaryView.vue')
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    linkActiveClass: 'active',
    routes
})

router.beforeEach((to, from, next) => {
    const goingToAuthenticatedRoute = (to.name !== 'login' && to.name !== 'register')
    const goingToLoginOrRegister = (to.name === 'login' || to.name === 'register')

    if (goingToAuthenticatedRoute && !store.getters.isLoggedIn) {
        return next({name: 'login'})
    }

    if (goingToLoginOrRegister && store.getters.isLoggedIn) {
        return next({name: 'board'})
    }

    return next()
})

router.afterEach((to) => {
    document.title = to.meta.title + ' | Kanban'
})

export default router
