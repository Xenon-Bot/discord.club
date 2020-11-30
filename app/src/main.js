import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './state'
import 'bootstrap';
import './bootstrap.scss';
import '@fortawesome/fontawesome-free/js/all.js';
import LoginPrompt from './components/LoginPrompt.vue'

Vue.config.productionTip = false
Vue.component('login-prompt', LoginPrompt)

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')