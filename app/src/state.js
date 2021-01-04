import Vue from 'vue'
import Vuex from 'vuex'


Vue.use(Vuex)
const apiHost = process.env.VUE_APP_API_HOST;


class Api {
    constructor() {
        this.token = localStorage.getItem("token");
    }

    isAuthenticated() {
        return this.token !== undefined && this.token !== null
    }

    setToken(token) {
        this.token = token
        localStorage.setItem("token", token)
    }

    deleteToken() {
        localStorage.removeItem('token')
    }

    request(method, path, data) {
        const headers = {
            "Authorization": this.token
        }
        if (!(data instanceof FormData)) {
            headers['Content-Type'] = 'application/json'
        }
        const body = data instanceof FormData ? data : JSON.stringify(data)

        return fetch(apiHost + path, {
            method: method,
            headers: headers,
            body: body
        })
            .then(resp => {
                if (!resp.ok) {
                    // NotificationManager.error(`API Error ${resp.status}: ${resp.statusText}`);
                    if (!resp.ok) {
                        if (resp.status === 401) {
                            this.token = null;
                            localStorage.removeItem("token");
                        }
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
        return this.request('POST', '/oauth/exchange', {code})
            .then(resp => {
                if (resp.ok) {
                    resp.json().then(data => this.setToken(data.token))
                }
                return resp
            })
    }

    getUser() {

    }

    getMessages() {
        return this.request('GET', '/messages')
    }

    getMessage(id) {
        return this.request('GET', `/messages/${id}`)
    }

    getFile(id) {
        return this.request('GET', `/messages/files/${id}`)
    }

    saveMessage(name, data) {
        const formData = new FormData()
        formData.append('json', JSON.stringify(data.json))
        formData.append('name', name)
        for (let i in data.files) {
            let file = data.files[i]
            formData.append(`file${i}`, file.content, file.name)
        }
        return this.request('POST', `/messages`, formData)
    }

    editMessage(id, data) {
        const formData = new FormData()
        formData.append('json', JSON.stringify(data.json))
        for (let i in data.files) {
            let file = data.files[i]
            formData.append(`file${i}`, file.content, file.name)
        }
        return this.request('PATCH', `/messages/${id}`, formData)
    }

    deleteMessage(id) {
        return this.request('DELETE', `/messages/${id}`)
    }

    createShare(json) {
        return this.request('POST', '/messages/share', {json: json})
    }

    getShare(id) {
        return this.request('GET', `/messages/share/${id}`)
    }

    getIntegrations() {
        return this.request('GET', '/integrations')
    }

    getIntegration(id) {
        return this.request('GET', `/integrations/${id}`)
    }

    deleteIntegration(id) {
        return this.request('DELETE', `/integrations/${id}`)
    }

    createIntegration(data) {
        return this.request('POST', '/integrations', data)
    }

    editIntegration(id, data) {
        return this.request('PATCH', `/integrations/${id}`, data)
    }

    getTriggers() {
        return this.request('GET', '/triggers')
    }

    getTrigger(id) {
        return this.request('GET', `/triggers/${id}`)
    }

    createTrigger(data) {
        return this.request('POST', '/triggers', data)
    }

    editTrigger(id, data) {
        return this.request('PATCH', `/triggers/${id}`, data)
    }
}


const store = new Vuex.Store({
    state: {
        api: new Api(),
        user: null,
        settings: {
            enableProxy: localStorage.getItem('enableProxy') !== 'false'
        }
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
    }
})

export default store