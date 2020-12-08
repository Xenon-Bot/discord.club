<template>
    <div class="modal fade" tabindex="-1" role="dialog" ref="modal">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Confirm Action</h5>
                </div>
                <div class="modal-body">
                    <p>{{text}}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal" v-on:click="onCancel">Cancel</button>
                    <button type="button" class="btn btn-primary" v-on:click="onConfirm" data-dismiss="modal">Confirm
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import $ from 'jquery'

    export default {
        name: 'Confirmation',
        props: ['text'],
        data() {
            return {
                result: null,
                resolve: null,
                reject: null
            }
        },
        methods: {
            open() {
                $(this.$refs.modal).modal({backdrop: 'static'})
                this.result = null
                return new Promise(function(resolve, reject) {
                    this.resolve = resolve
                    this.reject = reject
                }.bind(this))
            },
            onConfirm() {
                this.result = true
                this.resolve(true)
            },
            onCancel() {
                this.result = false
                this.resolve(false)
            }
        }
    }
</script>