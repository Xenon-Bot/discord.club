<template>
    <div>
        <editor v-bind:onSave="onSave" ref="editor"></editor>
        <div class="modal fade" id="saveModal" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Save Message</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <label>Message Name</label>
                        <input type="text" class="form-control" placeholder="Cool Message" v-model.trim="saveName">
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" v-on:click="saveMessage"
                                v-bind:class="{disabled: !saveName}">Save
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import Editor from '@/components/Editor.vue'
    import $ from 'jquery'

    export default {
        name: 'QuickMessage',
        components: {Editor},
        data() {
            return {
                saveName: ""
            }
        },
        methods: {
            onSave() {
                $('#saveModal').modal()
            },
            saveMessage() {
                if (!this.saveName) return;
                let payload = {
                    data: this.$refs.editor.getJSON(),
                    files: this.$refs.editor.files,
                    name: this.saveName
                }
                this.api.saveMessage(payload)
            }
        },
        computed: {
            api() {
                return this.$store.state.api
            }
        }
    }
</script>