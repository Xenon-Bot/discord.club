<template>
    <div>
        <editor v-bind:onSave="onSave"/>
    </div>
</template>
<script>
    import Editor from '@/components/Editor.vue'

    export default {
        name: 'EditMessage',
        components: {Editor},
        methods: {
            onSave() {
            }
        },
        computed: {
            api() {
                return this.$store.state.api
            }
        }
    }
</script>