<template>
    <div>
        <editor v-bind:onSave="onSave" v-bind:localStorage="false" ref="editor"/>
    </div>
</template>
<script>
    import Editor from '@/components/Editor.vue'

    export default {
        name: 'EditMessage',
        components: {Editor},
        methods: {
            onSave() {
                let payload = {
                    data: this.$refs.editor.getJSON(),
                    files: this.$refs.editor.files
                }
                this.api.editMessage(this.msgId, payload).then(resp => console.log(resp))
            }
        },
        created() {
            this.api.getMessage(this.msgId).then(resp => {
                if (!resp.ok) {
                    console.log(resp)
                } else {
                    resp.json().then(body => {
                        this.$refs.editor.setJSON(body.data)
                        this.$refs.editor.files = body.files
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