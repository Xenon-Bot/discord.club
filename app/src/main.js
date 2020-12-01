import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './state'
import 'bootstrap';
import '@fortawesome/fontawesome-free/js/all.js';
import LoginPrompt from './components/LoginPrompt.vue'
import Loading from './components/Loading.vue'
import Notifications from 'vue-notification'
import './bootstrap.scss';

Vue.config.productionTip = false
Vue.use(Notifications)
Vue.component('login-prompt', LoginPrompt)
Vue.component('loading', Loading)

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')