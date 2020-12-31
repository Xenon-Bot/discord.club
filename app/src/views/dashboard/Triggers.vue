<template>
    <div>
        <login-prompt v-if="!api.isAuthenticated()"/>
        <trigger-editor/>
    </div>
</template>

<script>
    import TriggerEditor from "@/components/TriggerEditor";

    export default {
        components: {TriggerEditor},
        computed: {
            api() {
                return this.$store.state.api
            }
        }
    }
</script>