<template>
    <div>
        <div v-if="integrations.length > 0">
            <div v-for="(integration, i) in integrations" :key="i" class="card bg-darker mb-3">
                <div class="card-body">
                    <div class="float-right">
                        <button class="btn btn-outline-primary mr-2">Edit</button>
                        <button class="btn btn-outline-secondary">Delete</button>
                    </div>
                    <h5 class="align-middle mb-0">{{integration.name}}
                        <span class="text-muted">-
                            <span v-if="integration.type === 0">Discord Bot</span>
                        </span>
                    </h5>
                    <div class="float-clear"></div>
                </div>
            </div>
        </div>
        <h3 v-else>
            You don't have any integrations yet
        </h3>
        <button class="btn btn-outline-secondary float-right" @click="openAddModal">Add Integration</button>

        <div class="modal fade" ref="editModal" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h4 class="modal-title">
                            <span v-if="editing.id">Edit</span>
                            <span v-else>Add</span>
                            Integration</h4>
                    </div>
                    <div class="modal-body">
                        <div class="form-row">
                            <div class="col-12 col-sm-4 mb-4">
                                <label>Type</label>
                                <select class="custom-select" v-model="editing.type">
                                    <option :value="0">Discord Bot</option>
                                </select>
                            </div>
                            <div class="col-12 col-sm-8 mb-4">
                                <label>Name</label>
                                <input type="text" class="form-control" placeholder="Account XY" v-model="editing.name">
                            </div>
                        </div>
                        <div v-if="editing.type === 0">
                            <label>Client ID</label>
                            <input type="number" class="form-control mb-3" v-model="editing.values.client_id">
                            <label>Bot Token</label>
                            <input type="password" class="form-control mb-3" v-model="editing.values.bot_token">
                            <label>Public Key</label>
                            <input type="text" class="form-control mb-4" v-model="editing.values.public_key">
                        </div>

                        <div class="float-right">
                            <button type="button" class="btn btn-secondary mr-2" data-dismiss="modal">Close</button>
                            <button class="btn btn-primary" @click="saveIntegration">Save Integration</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import $ from 'jquery'

    export default {
        name: 'Integrations',
        data() {
            return {
                integrations: [],
                editing: {values: {}, type: 0}
            }
        },
        mounted() {
            this.api.getIntegrations()
                .then(resp => resp.json())
                .then(data => this.integrations = data)
        },
        methods: {
            openAddModal() {
                this.editing = {values: {}, type: 0}
                $(this.$refs.editModal).modal()
            },
            saveIntegration() {
                if (this.editing.id) {
                    console.log('edit')
                } else {
                    this.api.createIntegration(this.editing)
                        .then(resp => {
                            if (resp.ok) {
                                this.$notify({
                                    group: 'main',
                                    title: 'Integration Saved',
                                    text: 'The integration was saved and can now be used in triggers',
                                    type: 'success'
                                })
                                // TODO: validate values
                                $(this.$refs.editModal).modal('hide')
                            }
                        })
                }
            }
        },
        computed: {
            api() {
                return this.$store.state.api
            }
        }
    }
</script>