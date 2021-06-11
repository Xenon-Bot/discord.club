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
                <button class="btn btn-outline-secondary" v-on:click="onSave" type="button">
                    Save Message
                </button>
            </template>
        </editor>
        <div class="modal fade" id="saveModal" tabindex="-1" role="dialog">
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
                        <input type="text" class="form-control mb-3" placeholder="Cool Message" v-model.trim="saveName">
                        <span class="text-muted">Saved messages don't include the webhook or message URL.</span>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" v-on:click="saveMessage" data-dismiss="modal"
                                :class="{disabled: !saveName}" :disabled="!saveName">Save
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
    import $ from 'jquery'
    import WebhookExecutor from "@/components/WebhookExecutor";

    export default {
        name: 'QuickMessage',
        components: {Editor, WebhookExecutor},
        created() {
            const lastData = localStorage.getItem("lastJson")
            if (lastData) {
                this.initData = {json: JSON.parse(lastData)}
            }
        },
        data() {
            return {
                saveName: "",
                initData: null,
                lastData: {}
            }
        },
        methods: {
            onDataUpdate(data) {
                this.lastData = data
                localStorage.setItem("lastJson", JSON.stringify(this.lastData.json))
            },
            onSave() {
                $('#saveModal').modal()
            },
            onMessageRetrieved(data) {
                this.initData = {files: [], json: data}
            },
            saveMessage() {
                if (!this.saveName) return;
                this.api.saveMessage(this.saveName, this.lastData).then(resp => {
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
            }
        },
        computed: {
            api() {
                return this.$store.state.api
            }
        }
    }
</script>