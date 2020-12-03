<template>
    <div>
        <login-prompt v-if="!api.isAuthenticated()"/>
        <div v-else>
            <div v-if="loadingError">{{loadingError}}</div>
            <loading v-else-if="!messages"/>
            <div v-else-if="messages.length === 0">
                <h5>You don't have any messages yet :(</h5>
            </div>
            <div v-else class="row">
                <div v-for="(msg, i) in messages" v-bind:key="i" class="col-12 mb-2">
                    <div class="card bg-darker">
                        <div class="card-body">
                            <div class="float-right">
                                <router-link v-bind:to="'/dashboard/messages/' + msg.id">
                                    <button class="btn btn-outline-primary mr-2">View</button>
                                </router-link>
                                <button class="btn btn-outline-secondary" v-on:click="deleteMessage(msg.id)">Delete
                                </button>
                            </div>
                            <h5 class="c-pointer align-middle mb-0" data-toggle="collapse"
                                v-bind:data-target="'#msg' + i">{{msg.name}}</h5>
                            <span class="text-muted timestamp">{{unixTimestampToString(msg.last_updated)}}</span>
                            <div class="float-clear"></div>
                        </div>
                        <div class="collapse bg-discordbg rounded-bottom" v-bind:id="'msg' + i">
                            <preview v-bind:data="msg" class="mx-3 my-4"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal fade" id="sendModal" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Send Message</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="form-row mb-2">
                            <div class="col-12 mb-4">
                                <label>Webhook URL</label>
                                <input v-model.trim.lazy="webhookUrl" type="url" class="form-control"
                                       placeholder="https://discord.com/api/webhooks/423157583646294017/nsFEJfuNKVBRcKcgj0JX3TygdvhX-ItEJhrWVWadw7shUXXuIRwsJHUS_XbDDSA_ILKN">
                            </div>
                            <div class="col-12 mb-4">
                                <label>Message ID or URL
                                    <span class="ml-1 hover-tooltip">
                                    <i class="fas fa-question hover-tooltip-trigger"/>
                                    <span class="hover-tooltip-content bg-dark py-2 px-3 rounded">
                                        If you want to edit an existing message, you can paste the message link or id here.
                                        The author of the message must be a webhook.
                                    </span>
                                </span>
                                </label>
                                <input v-model.trim.lazy="messageUrl" type="text" class="form-control"
                                       placeholder="https://discord.com/channels/410488579140354049/633228954064650250/781981855808487477">
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" data-dismiss="modal" v-bind:class="{disabled: !webhookUrl}" v-on:click="sendMessage">
                            <span v-if="messageId">Edit</span>
                            <span v-else>Send</span>
                            Message
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import Preview from '@/components/Preview.vue'
    import $ from 'jquery'

    export default {
        name: 'Messages',
        components: {Preview},
        data() {
            return {
                messages: null,
                loadingError: null,
                webhookId: null,
                webhookToken: null,
                messageId: null,
                toSend: null
            }
        },
        created() {
            if (this.api.isAuthenticated()) {
                this.loadMessages()
            }
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
            },
            deleteMessage(id) {
                this.api.deleteMessage(id).then(resp => {
                    if (!resp.ok) {
                        console.log(resp)
                    } else {
                        this.loadMessages()
                    }
                })
            },
            sendModal(i) {
                this.toSend = i
                $('#sendModal').modal()
            },
            sendMessage() {
                let msg = this.messages[this.toSend]
                console.log(msg)
            }
        },
        computed: {
            api() {
                return this.$store.state.api
            },
            messageUrl: {
                get() {
                    return this.messageId
                },
                set(newValue) {
                    const urlRegex = /https:\/\/(canary\.)?discord(app)?.com\/channels\/[0-9]+\/[0-9]+\/([0-9]+)\/?/i
                    let match = newValue.toString().match(urlRegex);
                    if (match) {
                        this.messageId = match[3]
                    } else if (newValue.match(/^[0-9]+$/)) {
                        this.messageId = newValue
                    } else {
                        this.messageId = null;
                    }
                }
            },
            webhookUrl: {
                get() {
                    if (this.webhookId && this.webhookToken) {
                        return `https://discord.com/api/v8/webhooks/${this.webhookId}/${this.webhookToken}`
                    }
                    return null
                },
                set(newValue) {
                    const urlRegex = /https:\/\/(canary\.)?discord(app)?.com\/(api\/(v[6-8]\/)?)?webhooks\/([0-9]+)\/(.+)\/?/i
                    let match = newValue.match(urlRegex);
                    if (match) {
                        this.webhookId = match[5]
                        this.webhookToken = match[6]
                    } else {
                        this.webhookId = null
                        this.webhookToken = null
                    }
                }
            }
        }
    }
</script>
<style scoped lang="scss">
    .timestamp {
        font-size: 0.8em;
    }
</style>