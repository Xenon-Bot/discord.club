<template>
    <div class="modal fade" id="saveModal" tabindex="-1" role="dialog" ref="modal">
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
                $(this.$refs.modal).modal()
                this.result = null
                const refBack = this
                return new Promise(function(resolve, reject) {
                    refBack.resolve = resolve
                    refBack.reject = reject
                })
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