<template>
    <div>
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
        <div class="float-right">
            <button class="btn btn-outline-secondary mr-2" v-on:click="editMessage" type="button"
                    :class="{disabled: !webhookUrl}" :disabled="!webhookUrl" v-if="messageId">
                <span v-if="editDone" class="mr-1"><i class="fas fa-check-circle"/></span>
                Edit Message
            </button>
            <button class="btn btn-outline-primary" v-on:click="sendMessage" type="button"
                    :class="{disabled: !webhookUrl}" :disabled="!webhookUrl">
                <span v-if="sendDone" class="mr-1"><i class="fas fa-check-circle"/></span>
                Send Message
            </button>
        </div>


        <div class="modal fade" id="responseModal" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Webhook Error</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <error-formatter :response="response"/>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
        <confirmation
                text="Do you want to load the JSON-Code from the existing message? This will overwrite your existing message!"
                ref="existingOverwriteConfirmation"/>
    </div>
</template>
<script>
    import $ from "jquery";
    import Confirmation from "./Confirmation";
    import ErrorFormatter from './ErrorFormatter'

    export default {
        name: 'SendMessage',
        props: ['data'],
        components: {Confirmation, ErrorFormatter},
        data() {
            return {
                webhookId: "",
                webhookToken: "",
                messageId: "",
                response: null,

                sendDone: false,
                editDone: false
            }
        },
        methods: {
            formatError(data) {
                if (!data.errors) {
                    return 'Unknown error'
                }

                let result = ''
                for (let error of data.errors) {
                    console.log(error)
                }
                return result
            },
            sendMessage() {
                if (!this.webhookUrl) return
                let data = new FormData()
                data.append('payload_json', JSON.stringify(this.data.json))
                for (let i in this.data.files) {
                    let file = this.data.files[i]
                    data.append(`file${i}`, file.content, file.name)
                }

                this.sendDone = false
                try {
                    fetch(`${this.webhookUrl}?wait=true`, {
                        method: 'POST',
                        body: data
                    })
                        .then(resp => {
                            this.response = resp
                            if (resp.ok) {
                                this.sendDone = true
                                setTimeout(() => this.sendDone = false, 2000)
                                resp.json().then(data => {
                                    this.messageId = data.id
                                })
                            } else {
                                $('#responseModal').modal()
                            }
                        })
                } catch (e) {
                    alert(e)
                }
            },
            editMessage() {
                if (!this.messageId || !this.webhookUrl) return
                let payload = this.data.json
                if (!payload.content) {
                    payload.content = ' '
                }

                this.editDone = false
                try {
                    fetch(`${this.webhookUrl}/messages/${this.messageId}`, {
                        method: 'PATCH',
                        body: JSON.stringify(payload),
                        headers: {'Content-Type': 'application/json'}
                    })
                        .then(resp => {
                            this.response = resp
                            if (!resp.ok) {
                                $('#responseModal').modal()
                            } else {
                                this.editDone = true
                                setTimeout(() => this.editDone = false, 1000)
                            }
                        })
                } catch (e) {
                    alert(e)
                }
            }
        },
        computed: {
            messageUrl: {
                get() {
                    return this.messageId
                },
                set(newValue) {
                    const urlRegex = /https:\/\/((canary\.)|(ptb\.))?\.?discord(app)?.com\/channels\/[0-9]+\/[0-9]+\/([0-9]+)\/?/i
                    let match = newValue.toString().match(urlRegex);
                    if (match) {
                        this.messageId = match[5]
                    } else if (newValue.match(/^[0-9]+$/)) {
                        this.messageId = newValue
                    } else {
                        this.messageId = null;
                    }

                    if (this.webhookUrl && this.messageId) {
                        fetch(`${this.webhookUrl}/messages/${this.messageId}`, {
                            method: 'PATCH',
                            body: '{}',
                            headers: {'Content-Type': 'application/json'}
                        })
                            .then(resp => {
                                if (!resp.ok) {
                                    this.$notify({
                                        group: 'main',
                                        title: 'Unknown message',
                                        text: `The message is either invalid or wasn't sent by the webhook you specified.`,
                                        type: 'error'
                                    })
                                } else {
                                    resp.json().then(data => {
                                        this.$refs.existingOverwriteConfirmation.open().then(confirmed => {
                                            if (confirmed) {
                                                this.$emit('messageRetrieved', data)
                                            }
                                        })
                                    })
                                }
                            })
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
                    const urlRegex = /https:\/\/((canary\.)|(ptb\.))?discord(app)?.com\/(api\/(v[6-8]\/)?)?webhooks\/([0-9]+)\/(.+)\/?/i
                    let match = newValue.match(urlRegex);
                    if (match) {
                        this.webhookId = match[7]
                        this.webhookToken = match[8]
                        fetch(this.webhookUrl)
                            .then(resp => resp.json())
                        // .then(data => this.$refs.editor.webhookUsername = data.name)
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
    .spin {
        animation-name: spin;
        animation-duration: 500ms;
        animation-iteration-count: infinite;
        animation-timing-function: linear;
    }

    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
</style>