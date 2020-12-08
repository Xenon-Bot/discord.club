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
            <button class="btn btn-outline-secondary mr-2" v-on:click="editMessage"
                    :class="{disabled: !webhookUrl}" :disabled="!webhookUrl" v-if="messageId">
                Edit Message
            </button>
            <button class="btn btn-outline-primary" v-on:click="sendMessage"
                    :class="{disabled: !webhookUrl}" :disabled="!webhookUrl">
                Send Message
            </button>
        </div>


        <div class="modal fade" id="responseModal" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{responseStatus}}</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <textarea class="form-control disabled bg-darker" rows="10" v-bind:value="responseBody"
                                  disabled/>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
        <confirmation text="Do you want to load the JSON-Code from the existing message? This will overwrite your existing message!" ref="existingOverwriteConfirmation"/>
    </div>
</template>
<script>
    import $ from "jquery";
    import Confirmation from "./Confirmation";

    export default {
        name: 'SendMessage',
        props: ['data'],
        components: {Confirmation},
        data() {
            return {
                webhookId: "",
                webhookToken: "",
                messageId: "",
                responseStatus: "",
                responseBody: ""
            }
        },
        methods: {
            sendMessage() {
                if (!this.webhookUrl) return
                let data = new FormData()
                data.append('payload_json', JSON.stringify(this.data.json))
                for (let i in this.data.files) {
                    let file = this.data.files[i]
                    data.append(`file${i}`, file.content, file.name)
                }

                fetch(`${this.webhookUrl}?wait=true`, {
                    method: 'POST',
                    body: data
                })
                    .then(resp => {
                        resp.json().then(data => {
                            this.responseStatus = `${resp.statusText} (${resp.status})`
                            this.responseBody = JSON.stringify(data, null, 2)
                            $('#responseModal').modal()

                            if (resp.ok) {
                                this.messageId = data.id
                            }
                        })
                    })
            },
            editMessage() {
                if (!this.messageId || !this.webhookUrl) return
                let payload = this.data.json
                if (!payload.content) {
                    payload.content = ' '
                }

                // TODO: default content to " " to remove existing content
                fetch(`${this.webhookUrl}/messages/${this.messageId}`, {
                    method: 'PATCH',
                    body: JSON.stringify(payload),
                    headers: {'Content-Type': 'application/json'}
                })
                    .then(resp => {
                        resp.json().then(data => {
                            this.responseStatus = `${resp.statusText} (${resp.status})`
                            this.responseBody = JSON.stringify(data, null, 2)
                            $('#responseModal').modal()
                        })
                    })
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
                                    alert("Invalid message")
                                }
                                return resp.json()
                            })
                            .then(data => {
                                this.$refs.existingOverwriteConfirmation.open().then(confirmed => {
                                    if (confirmed) {
                                        this.$emit('messageRetrieved', data)
                                    }
                                })
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
                    console.log(match)
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

</style>