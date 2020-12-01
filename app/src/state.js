import Vue from 'vue'
import Vuex from 'vuex'


Vue.use(Vuex)
const apiHost = "http://localhost:8080/api";


class Api {
    constructor() {
        this.token = localStorage.getItem("token");
    }

    isAuthenticated() {
        return this.token !== undefined && this.token !== null
    }

    setToken(token) {
        this.token = token
    }

    request(method, path, data) {
        return fetch(apiHost + path, {
            method: method,
            headers: {
                "Content-Type": "application/json",
                "Authorization": this.token
            },
            body: data != null ? JSON.stringify(data) : null
        })
            .then(resp => {
                if (!resp.ok) {
                    // NotificationManager.error(`API Error ${resp.status}: ${resp.statusText}`);
                    if (!resp.ok) {
                        if (resp.status === 401) {
                            this.token = null;
                            localStorage.removeItem("token");
                        } else {
                            resp.json().then(data => {
                                Vue.notify({
                                    group: 'main',
                                    title: 'Request Failed',
                                    text: data.error,
                                    type: 'error'
                                })
                            }).catch(() => {
                                Vue.notify({
                                    group: 'main',
                                    title: 'Request Failed',
                                    text: `${resp.status}: ${resp.statusText}`,
                                    type: 'error'
                                })
                            })
                        }
                    }
                }
                return resp
            })
            .catch(() => {
                Vue.notify({
                    group: 'main',
                    title: 'Request Failed',
                    text: 'The API seems to be unavailable',
                    type: 'error'
                })
            })
    }

    exchangeToken(code) {
        console.log(code)
    }

    getUser() {

    }

    getMessages() {
        return this.request('GET', '/messages')
    }

    getMessage(id) {
        return this.request('GET', `/messages/${id}`)
    }

    saveMessage(payload) {
        return this.request('POST', `/messages`, payload)
    }

    editMessage(id, payload) {
        return this.request('PATCH', `/messages/${id}`, payload)
    }

    deleteMessage(id) {
        return this.request('DELETE', `/messages/${id}`)
    }
}


const store = new Vuex.Store({
    state: {
        api: new Api(),
        user: null
    },
    mutations: {
        init(state) {
            state.api.getUser()
                .then(resp => resp.json())
                .then(data => state.user = data)
        },
        login(state, token) {
            state.api.setToken(token);
            localStorage.setItem("token", token)
            this.init(state);
        }
    },
    getters: {
        isAuthenticated(state) {
            return state.api.isAuthenticated()
        }
    }
})

export default store