<template>
    <div>
        <editor v-on:save="onSave" v-on:dataUpdate="onDataUpdate" :initData="initData">
            <template v-slot:top-left>
                <h4 class="ml-2 mb-3">Webhook</h4>
                <div class="card border-0 tex-light mb-4 bg-darker">
                    <div class="card-body mb-0">
                        <webhook-executor :data="lastData" v-on:messageRetrieved="onMessageRetrieved"/>
                    </div>
                </div>
            </template>
            <template v-slot:save>
                <button class="btn btn-outline-secondary mr-2" v-on:click="onSaveAs" type="button">
                    Save As
                </button>
                <button class="btn btn-outline-secondary" v-on:click="onSave" type="button">
                    Save Message
                </button>
            </template>
        </editor>
        <confirmation text="Are you sure that you want to leave this page? You have unsaved changes!"
                      ref="exitConfirmation"/>

        <div class="modal fade" id="saveAsModal" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content" v-if="api.isAuthenticated()">
                    <div class="modal-header">
                        <h5 class="modal-title">Save Message</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <label>Message Name</label>
                        <input type="text" class="form-control mb-3" placeholder="Cool Message"
                               v-model.trim="saveAsName">
                        <span class="text-muted">Saved messages don't include the webhook or message URL.</span>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" v-on:click="saveMessageAs" data-dismiss="modal"
                                :class="{disabled: !saveAsName}" :disabled="!saveAsName">Save
                        </button>
                    </div>
                </div>
                <div class="modal-content" v-else>
                    <login-prompt/>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import Editor from '@/components/Editor.vue'
    import WebhookExecutor from "@/components/WebhookExecutor";
    import Confirmation from "@/components/Confirmation";
    import $ from "jquery";

    export default {
        name: 'EditMessage',
        components: {Editor, WebhookExecutor, Confirmation},
        data() {
            return {
                lastData: {},
                initData: null,
                unsavedChanges: false,

                saveAsName: ''
            }
        },
        created() {
            this.api.getMessage(this.msgId).then(resp => {
                if (!resp.ok) {
                    console.log(resp)
                } else {
                    resp.json().then(data => {
                        this.initData = data
                        for (let file of data.files) {
                            this.api.getFile(file.id)
                                .then(resp => resp.blob())
                                .then(body => file.content = body)
                        }

                        setTimeout(() => this.unsavedChanges = false, 500)
                    })
                }
            })
        },
        mounted() {
            window.onbeforeunload = event => {
                if (this.unsavedChanges) {
                    event.preventDefault()
                    event.returnValue = "Are you sure that you want to leave this page? You have unsaved changes!"
                    return event.returnValue
                }
            }
        },
        beforeRouteLeave(to, from, next) {
            if (!this.unsavedChanges) {
                window.onbeforeunload = undefined
                return next()
            }

            this.$refs.exitConfirmation.open().then(confirmed => {
                if (confirmed) {
                    window.onbeforeunload = undefined
                    return next()
                }
            })
        },
        methods: {
            onDataUpdate(data) {
                this.lastData = data
                this.unsavedChanges = true
            },
            onSave() {
                this.api.editMessage(this.msgId, this.lastData).then(resp => {
                    if (!resp.ok) {
                        console.log(resp)
                    } else {
                        this.unsavedChanges = false
                        this.$notify({
                            group: 'main',
                            title: 'Messages Saved',
                            text: 'You can continue editing your message now',
                            type: 'success'
                        })
                    }
                })
            },
            onSaveAs() {
                $('#saveAsModal').modal()
            },
            saveMessageAs() {
                if (!this.saveAsName) return;
                this.api.saveMessage(this.saveAsName, this.lastData).then(resp => {
                    if (!resp.ok) {
                        console.log(resp)
                    } else {
                        this.$notify({
                            group: 'main',
                            title: 'Messages Saved',
                            text: 'You can continue editing your message now',
                            type: 'success'
                        })
                        resp.json().then(data => this.$router.push(`/dashboard/messages/${data.id}`))
                    }
                })
            },
            onMessageRetrieved(data) {
                this.initData = {files: [], json: data}
            },
        },
        computed: {
            api() {
                return this.$store.state.api
            },
            msgId() {
                return this.$route.params.id
            }
        }
    }
</script>