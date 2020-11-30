<template>
<div>
    <login-prompt v-if="!api.isAuthenticated"></login-prompt>
    <div v-else>
        <div v-if="loadingError">{{loadingError}}</div>
        <div v-else-if="!messages">Loading messages ...</div>
        <div v-else class="row">
            <div v-for="(msg, i) in messages" v-bind:key="i" class="col-12 mb-2">
                <div class="card bg-darker">
                    <div class="card-body">
                        <div class="float-right">
                            <router-link v-bind:to="'/dashboard/messages/' + msg.id">
                                <button class="btn btn-outline-secondary mr-2">Edit</button>
                            </router-link>
                            <button class="btn btn-outline-primary">Send</button>
                        </div>
                        <h5 class="c-pointer align-middle mb-0" data-toggle="collapse" v-bind:data-target="'#msg' + i">{{msg.name}}</h5>
                        <span class="text-muted timestamp">{{unixTimestampToString(msg.last_updated)}}</span>
                        <div class="float-clear"></div>
                    </div>
                    <div class="collapse bg-discordbg rounded-bottom" v-bind:id="'msg' + i">
                        <preview v-bind:data="msg.data" class="mx-3 my-4"></preview>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>
<script>
import Preview from '@/components/Preview.vue'

export default {
    name: 'Messages',
    components: {Preview},
    data() {
        return {
            messages: null,
            loadingError: null
        }
    },
    created() {
        this.loadMessages()
    },
    methods: {
        loadMessages() {
            this.messages = null
            this.loadingError = null
            this.api.getMessages().then(resp => {
                if (!resp.ok) {
                    this.loadingError = `API Error: ${resp.statusText}`
                } else {
                    resp.json().then(data => this.messages = data)
                }
            })
        },
        unixTimestampToString(timestamp) {
            if (!timestamp) {
                return timestamp
            }
            let date = new Date(timestamp * 1000)
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString().replace(/(.*)\D\d+/, '$1');
        }
    },
    computed: {
        api() { return this.$store.state.api }
    }
}
</script>
<style scoped lang="scss">
.timestamp {
    font-size: 0.8em;
}
</style>