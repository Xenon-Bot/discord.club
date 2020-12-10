import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './views/Home.vue'
import Index from "./views/Index";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        component: Home,
        children: [
            {
                name: 'Index',
                path: '',
                component: Index
            },
            {
                name: 'Privacy Policy',
                path: '/privacy',
                component: () =>
                    import ( /* webpackChunkName: "privacy" */ './views/Privacy.vue')
            },
            {
                name: 'About',
                path: '/about',
                component: () =>
                    import ( /* webpackChunkName: "about" */ './views/About.vue')
            }
        ]
    },
    {
        path: '/dashboard',
        alias: ['/embedg', '/embed-generator'],
        component: () =>
            import ( /* webpackChunkName: "dashboard" */ './views/dashboard/Dashboard.vue'),
        children: [{
            name: 'Quick Message',
            path: '',
            component: () =>
                import ( /* webpackChunkName: "editor" */ './views/dashboard/QuickMessage.vue')
        },
            {
                name: 'Messages',
                path: 'messages',
                component: () =>
                    import ( /* webpackChunkName: "messages" */ './views/dashboard/Messages.vue')
            },
            {
                name: 'Edit Message',
                path: 'messages/:id',
                component: () =>
                    import ( /* webpackChunkName: "edit_message" */ './views/dashboard/EditMessage.vue')
            },
            {
                name: 'Triggers',
                path: 'triggers',
                component: () =>
                    import ( /* webpackChunkName: "triggers" */ './views/dashboard/Triggers.vue')
            },
            {
                name: 'Help & FAQ',
                path: 'docs',
                alias: ['/docs', '/help', 'help', 'faq', '/faq'],
                component: () =>
                    import ( /* webpackChunkName: "help" */ './views/dashboard/Help.vue')
            }
        ]
    },
    {
        path: '/callback',
        name: 'Oauth Callback',
        component: () =>
            import ( /* webpackChunkName: "oauth_callback" */ './views/OauthCallback.vue')
    },
    {
        path: '/share/:id',
        name: 'Share Shortcut',
        redirect: to => {
            return {path: '/dashboard', query: {share: to.params.id}}
        }
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router