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
        </editor>
        <confirmation text="Are you sure that you want to leave this page? You have unsaved changes!"
                      ref="exitConfirmation"/>
    </div>
</template>
<script>
    import Editor from '@/components/Editor.vue'
    import WebhookExecutor from "@/components/WebhookExecutor";
    import Confirmation from "@/components/Confirmation";

    export default {
        name: 'EditMessage',
        components: {Editor, WebhookExecutor, Confirmation},
        data() {
            return {
                lastData: null,
                initData: null,
                unsavedChanges: false,
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