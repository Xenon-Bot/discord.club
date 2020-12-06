<template>
    <div>
        <editor v-on:save="onSave" v-on:dataUpdate="onDataUpdate" :initData="initData">
            <template v-slot:top-left>
                <h4 class="ml-2 mb-3">Webhook</h4>
                <div class="card border-0 tex-light mb-4 bg-darker">
                    <div class="card-body mb-0">
                        <webhook-executor :data="lastData"/>
                    </div>
                </div>
            </template>
        </editor>
    </div>
</template>
<script>
    import Editor from '@/components/Editor.vue'
    import WebhookExecutor from "@/components/WebhookExecutor";

    export default {
        name: 'EditMessage',
        components: {Editor, WebhookExecutor},
        data() {
            return {
                lastData: null,
                initData: null,
                unsavedChanges: false,
            }
        },
        beforeRouteLeave(to, from, next) {
            if (this.unsavedChanges && !window.confirm('You have unsaved changes! Do you want to leave?')) {
                return;
            }
            next()
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
            }
        },
        created() {
            this.api.getMessage(this.msgId).then(resp => {
                if (!resp.ok) {
                    console.log(resp)
                } else {
                    resp.json().then(data => {
                        this.initData = data
                        this.unsavedChanges = false
                        for (let file of data.files) {
                            this.api.getFile(file.id)
                                .then(resp => resp.blob())
                                .then(body => file.content = body)
                        }
                    })
                }
            })
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