<template>
    <div class="row">
        <div class="col-12 col-lg-6">
            <h4 class="mb-3 ml-2">Settings</h4>
            <div class="card mb-4 bg-darker">
                <div class="card-header">
                    <div class="form-row mb-2">
                        <div class="col-6">
                            <label class="required">Name</label>
                            <input type="text" class="form-control" v-model="name" placeholder="My Trigger">
                        </div>
                        <div class="col-6">
                            <label>Type</label>
                            <select class="custom-select" v-model="type">
                                <option :value="0">Scheduled</option>
                                <option :value="1">Custom Command</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <div class="form-row mt-2" v-if="type === 0">
                        <div class="col-6 mb-3">
                            <label class="required">Start Time</label>
                            <datetime type="datetime" input-class="form-control" v-model.trim="settings.start"/>
                        </div>
                        <div class="col-6 mb-4">
                            <label class="required">Repeat (hours)</label>
                            <input type="number" class="form-control" v-model="settings.repeat" required>
                        </div>
                    </div>
                    <div class="form-row mt-2" v-if="type === 1">
                        <div class="col-12 mb-3">
                            <label class="required">Bot Integration</label>
                            <router-link to="/dashboard/integrations" class="float-right text-primary"
                                         @click="addCommandOption()">
                                <i class="fas fa-plus"/>
                            </router-link>
                            <select class="custom-select" v-model="settings.integration_id" required>
                                <option
                                        :value="integration.id"
                                        v-for="integration of integrations" :key="integration.id"
                                        :disabled="integration.type !== 0"
                                >{{integration.name}}
                                </option>
                            </select>
                        </div>
                        <div class="col-12 mb-4">
                            <label class="required">Guild ID</label>
                            <input type="text" class="form-control" v-model.trim="settings.guild_id"
                                   placeholder="91ed336ce046430857c1353a9886d8662a88a196f4aaf05194006648c645245c"
                                   required>
                        </div>
                    </div>

                    <div class="float-right mt-3">
                        <button class="btn btn-outline-primary" @click="saveTrigger">Save Trigger</button>
                    </div>
                </div>
            </div>
            <div v-if="type === 1 && settings.integration_id">
                <h4 class="mb-3 ml-2">Command</h4>
                <div class="card bg-darker">
                    <div class="card-body">
                        <label class="required">Name</label>
                        <input type="text" class="form-control mb-4" placeholder="ping" v-model="command.name" required>
                        <label class="required">Description</label>
                        <textarea rows="1" class="form-control mb-4" placeholder="My first ping command (pong!)"
                                  v-model="command.description" required/>
                        <label class="required">Show Command</label>
                        <select class="custom-select mb-4" v-model="command.show_source">
                            <option :value="true">Yes</option>
                            <option :value="false">No</option>
                        </select>
                        <h5 class="mb-3">Options</h5>
                        <div class="form-row mb-2" v-for="(option, o) in command.options" :key="`var${o}`">
                            <div class="col mb-2">
                                <input type="text" class="form-control" placeholder="Name" v-model.trim="option.name">
                            </div>
                            <div class="col mb-2">
                                <select class="custom-select" v-model="option.type">
                                    <option :value="3" selected>Text</option>
                                    <option :value="4">Number</option>
                                    <option :value="5">Boolean</option>
                                    <option :value="6">User</option>
                                    <option :value="7">Channel</option>
                                    <option :value="8">Role</option>
                                </select>
                            </div>
                            <div class="col-auto mb-2">
                                <div class="btn btn-outline-light" @click="deleteCommandOption(o)">
                                    <i class="fas fa-minus"/>
                                </div>
                            </div>
                            <div class="col-12 mb-3">
                                <textarea rows="1" class="form-control" placeholder="Description" v-model.trim="option.description"/>
                            </div>
                        </div>
                        <div>
                            <div class="btn btn-sm btn-outline-light mr-2" @click="clearCommandOptions()">
                                <i class="fas fa-trash"/>
                            </div>
                            <div class="btn btn-sm btn-outline-light" @click="addCommandOption()">
                                <i class="fas fa-plus"/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-12 col-lg-6">
            <h4 class="mb-3 ml-2">Actions</h4>
            <div v-for="(action, a) in actions" :key="`actions${a}`" class="card mb-3 bg-darker">
                <div class="card-body">
                    <div class="float-right">
                        <span class="mr-3 c-pointer" v-if="a !== 0" v-on:click="moveActionUp(a)"><i
                                class="fas fa-chevron-up"/></span>
                        <span class="mr-3 c-pointer" v-if="a !== actions.length - 1"
                              v-on:click="moveActionDown(a)"><i class="fas fa-chevron-down"/></span>
                        <span class="mr-3 c-pointer" v-if="actions.length < 5" v-on:click="cloneAction(a)"><i
                                class="far fa-copy"/></span>
                        <span class="mr-3 c-pointer" v-on:click="deleteAction(a)"><i
                                class="fas fa-minus"/></span>
                    </div>
                    <h5 class="c-pointer overflow-auto text-nowrap" data-toggle="collapse"
                        v-bind:data-target="'#action' + a" role="button">
                        <span class="mr-1">
                            <i class="fas fa-chevron-down"/>
                        </span>
                        Action {{a + 1}}
                        <span v-if="action.type === 0" class="text-muted">- Execute Webhook</span>
                        <span v-if="action.type === 1" class="text-muted">- Edit Webhook Message</span>
                        <span v-if="action.type === 2" class="text-muted">- Command Response</span>
                    </h5>
                    <div class="collapse mt-3" v-bind:id="'action' + a">
                        <div class="form-row">
                            <div class="col mb-4">
                                <label>Type</label>
                                <select class="custom-select" v-model="action.type">
                                    <option :value="0">Execute Webhook</option>
                                    <!-- <option :value="1">Edit Webhook Message</option> -->
                                    <option :value="2" :disabled="type !== 1">Command Response</option>
                                </select>
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="col-12 mb-4" v-if="action.type !== 2">
                                <label class="required">Webhook URL</label>
                                <input type="url" class="form-control" v-model.trim="action.webhook_url" required
                                       placeholder="https://discord.com/api/webhooks/423157583646294017/nsFEJfuNKVBRcKcgj0JX3TygdvhX-ItEJhrWVWadw7shUXXuIRwsJHUS_XbDDSA_ILKN">
                            </div>
                            <div class="col-12 mb-4" v-if="action.type === 1">
                                <label class="required">Message URL / ID</label>
                                <input type="url" class="form-control" v-model.trim="action.message_url" required
                                       placeholder="https://discord.com/channels/410488579140354049/633228954064650250/781981855808487477">
                            </div>
                            <div class="col-12 mb-4"
                                 v-if="action.type !== 2 || action.response_type === 3 || action.response_type === 4">
                                <label class="required">Message</label>
                                <div class="form-check float-right" v-if="action.type === 2">
                                    <input v-model.trim="action.response_ephemeral" type="checkbox"
                                           class="form-check-input">
                                    <label class="form-check-label">Ephemeral</label>
                                </div>
                                <select class="custom-select" v-model.trim="action.message_id" required>
                                    <option v-for="(msg, m) in messages" :key="`msg${m}`" :value="msg.id">{{msg.name}}
                                    </option>
                                </select>
                            </div>
                        </div>
                        <!--
                        <h5 class="mb-3">Variables</h5>
                        <div class="form-row mb-2" v-for="(variable, v) in action.variables" :key="`var${v}`">
                            <div class="col">
                                <input type="text" class="form-control" placeholder="Name" v-model.trim="variable.name">
                            </div>
                            <div class="col">
                                <input type="text" class="form-control" placeholder="Value"
                                       v-model.trim="variable.value">
                            </div>
                            <div class="col-auto">
                                <div class="btn btn-outline-light" @click="deleteVar(a, v)">
                                    <i class="fas fa-minus"/>
                                </div>
                            </div>
                        </div>
                        <div>
                            <div class="btn btn-sm btn-outline-light mr-2" @click="clearVars(a)">
                                <i class="fas fa-trash"/>
                            </div>
                            <div class="btn btn-sm btn-outline-light" @click="addVar(a)">
                                <i class="fas fa-plus"/>
                            </div>
                        </div>
                        -->
                    </div>
                </div>
            </div>
            <div class="float-right">
                <div class="btn btn-sm btn-outline-secondary mr-2" @click="clearActions">
                    <i class="fas fa-trash"/>
                </div>
                <div class="btn btn-sm btn-outline-primary" @click="addAction">
                    <i class="fas fa-plus"/>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import {Datetime} from 'vue-datetime'
    import 'vue-datetime/dist/vue-datetime.css'
    import $ from "jquery";

    export default {
        name: 'TriggerEditor',
        props: ['id'],
        components: {Datetime},
        data() {
            return {
                name: '',
                type: 0,
                settings: {},
                actions: [],
                messages: [],  // use in actions
                integrations: [], // use in actions and settings

                command: {
                    name: '',
                    description: '',
                    options: [],
                    show_source: true
                }  // only used in type 1
            }
        },
        mounted() {
            this.api.getMessages()
                .then(resp => resp.json())
                .then(data => this.messages = data)
            this.api.getIntegrations()
                .then(resp => resp.json())
                .then(data => this.integrations = data)
            if (this.id) {
                this.api.getTrigger(this.id)
                    .then(resp => resp.json())
                    .then(data => this.setTriggerData(data))
            }
        },
        methods: {
            addAction() {
                if (this.actions.length >= 5) {
                    return
                }
                this.actions.push({type: 0, message_id: null, response_type: 4, response_ephemeral: false})
                setTimeout(() => {
                    $(`#action${this.actions.length - 1}`).addClass('show')
                }, 100)
            },
            clearActions() {
                this.actions = []
            },
            deleteAction(i) {
                this.actions.splice(i, 1)
            },
            moveActionUp(i) {
                this.actions.splice(i - 1, 0, this.actions.splice(i, 1)[0])
            },
            moveActionDown(i) {
                this.actions.splice(i + 1, 0, this.actions.splice(i, 1)[0])
            },
            cloneAction(i) {
                if (this.actions.length >= 5) {
                    return
                }
                this.actions.splice(i + 1, 0, JSON.parse(JSON.stringify(this.actions[i])))
            },
            addVar(a) {
                const action = this.actions[a]
                if (!action.variables) {
                    action.variables = [{}]
                } else {
                    action.variables.push({})
                }
                this.$forceUpdate()
            },
            clearVars(a) {
                const action = this.actions[a]
                action.variables = []
                this.$forceUpdate()
            },
            deleteVar(a, v) {
                const action = this.actions[a]
                if (action.variables) {
                    action.variables.splice(v, 1)
                }
                this.$forceUpdate()
            },
            addCommandOption() {
                if (this.command.options) {
                    this.command.options.push({type: 3})
                } else {
                    this.command.options = [{type: 3}]
                }
            },
            deleteCommandOption(o) {
                if (this.command.options) {
                    this.command.options.splice(o, 1)
                }
            },
            clearCommandOptions() {
                this.command.options = []
            },
            saveTrigger() {
                if (this.id) {
                    console.log("save existing")
                } else {
                    console.log("save new")
                }
                // post or patch to discord api
            },
            setTriggerData(data) {
                this.name = data.name
                this.type = data.type
                this.settings = data.settings
                this.actions = data.actions

                if (this.type === 1) {
                    // fetch command if commandId is set
                }
            },
            getTriggerData() {
                return {
                    name: this.name,
                    type: this.type,
                    settings: this.settings,
                    actions: this.actions,
                }
            }
        },
        computed: {
            api() {
                return this.$store.state.api
            }
        },
        watch: {
            $data(newValue) {
                this.$emit('dataUpdate', newValue)
            }
        }
    }
</script>
<style>
    .vdatetime-popup {
        background-color: black;
        color: white;
    }

    .vdatetime-calendar__month__day:hover > span > span {
        background: #eee;
        color: black;
    }
</style>