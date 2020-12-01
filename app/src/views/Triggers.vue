<template>
    <div>
        <login-prompt v-if="!api.isAuthenticated()"/>
        <div v-else>
            <h1>Coming Soon</h1>
        </div>
    </div>
</template>

<script>
    export default {
        computed: {
            api() {
                return this.$store.state.api
            }
        }
    }
</script>