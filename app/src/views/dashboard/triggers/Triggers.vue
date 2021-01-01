<template>
    <div>
        <login-prompt v-if="!api.isAuthenticated()"/>
        <transition name="fade">
            <router-view/>
        </transition>
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