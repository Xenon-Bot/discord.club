<template>
    <div>
        <div v-if="integrations.length > 0">
            <div v-for="(integration, i) in integrations" :key="i" class="card bg-darker mb-3">
                <div class="card-body">
                    <div class="float-right">
                        <button class="btn btn-outline-primary mr-2" @click="openEditModal(i)">Edit</button>
                        <button class="btn btn-outline-secondary" @click="deleteIntegration(i)">Delete</button>
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
                            <span v-if="id">Edit</span>
                            <span v-else>Add</span>
                            Integration</h4>
                    </div>
                    <div class="modal-body">
                        <div class="form-row">
                            <div class="col-12 col-sm-4 mb-4">
                                <label>Type</label>
                                <select class="custom-select" v-model="type">
                                    <option :value="0">Discord Bot</option>
                                </select>
                            </div>
                            <div class="col-12 col-sm-8 mb-4">
                                <label class="required">Name</label>
                                <input type="text" class="form-control" placeholder="Account XY" v-model="name" required>
                            </div>
                        </div>
                        <div v-if="type === 0" class="mb-4">
                            <label class="required">Client ID</label>
                            <input type="text" class="form-control" v-model="values.client_id" required>
                            <label class="mt-3 required">Bot Token</label>
                            <input type="password" class="form-control" v-model="values.bot_token" required>
                            <label class="mt-3 required">Public Key</label>
                            <input type="text" class="form-control" v-model="values.public_key" required>
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

                type: 0,
                name: '',
                values: {}
            }
        },
        mounted() {
            this.loadIntegrations()
        },
        methods: {
            loadIntegrations() {
                this.api.getIntegrations()
                    .then(resp => resp.json())
                    .then(data => this.integrations = data)
            },
            deleteIntegration(i) {
                this.api.deleteIntegration(this.integrations[i].id).then(resp => {
                    if (resp.ok) {
                        this.integrations.splice(i, 1)
                    }
                })
            },
            openAddModal() {
                this.name = ''
                this.values = {}
                this.type = 0
                this.$forceUpdate();
                $(this.$refs.editModal).modal()
            },
            openEditModal(i) {
                const integration = this.integrations[i]

                this.id = integration.id
                this.name = integration.name
                this.values = integration.values

                this.$forceUpdate();
                $(this.$refs.editModal).modal()
            },
            saveIntegration() {
                // TODO: validate

                const payload = {type: this.type, name: this.name, values: this.values};
                if (this.id) {
                    this.api.editIntegration(this.id, payload)
                        .then(resp => {
                            if (resp.ok) {
                                this.$notify({
                                    group: 'main',
                                    title: 'Integration Saved',
                                    text: 'The integration was saved and can now be used in triggers',
                                    type: 'success'
                                })
                                $(this.$refs.editModal).modal('hide')
                                this.loadIntegrations()
                            }
                        })
                } else {
                    this.api.createIntegration(payload)
                        .then(resp => {
                            if (resp.ok) {
                                this.$notify({
                                    group: 'main',
                                    title: 'Integration Saved',
                                    text: 'The integration was saved and can now be used in triggers',
                                    type: 'success'
                                })
                                $(this.$refs.editModal).modal('hide')
                                this.loadIntegrations()
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
<style lang="scss">
    label.required::after {
        content: " *";
        vertical-align: bottom;
        font-size: 1em;
        font-style: italic;
        color: red;
    }
</style>