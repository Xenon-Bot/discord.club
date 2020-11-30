import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './views/Home.vue'

Vue.use(VueRouter)

const routes = [{
    path: '/',
    name: 'Home',
    component: Home
},
    {
        path: '/dashboard',
        component: () =>
            import ( /* webpackChunkName: "dashboard" */ './views/Dashboard.vue'),
        children: [{
            name: 'Quick Message',
            path: '',
            component: () =>
                import ( /* webpackChunkName: "editor" */ './views/QuickMessage.vue')
        },
            {
                name: 'Messages',
                path: 'messages',
                component: () =>
                    import ( /* webpackChunkName: "editor" */ './views/Messages.vue')
            },
            {
                name: 'Edit Message',
                path: 'messages/:id',
                component: () =>
                    import ( /* webpackChunkName: "editor" */ './views/EditMessage.vue')
            },
            {
                name: 'Triggers',
                path: 'triggers',
                component: () =>
                    import ( /* webpackChunkName: "editor" */ './views/Triggers.vue')
            }
        ]
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router