<template>
    <div class="container text-center mt-5">
        <div v-if="success">
            <h1>You are now logged in!</h1>
            <h5 class="text-muted">You can close this tab now ...</h5>
        </div>
        <div v-else-if="error">
            <h2>An error occurred while trying to log you in</h2>
            <h5 class="text-muted">You can close this tab now ...</h5>
        </div>
        <div v-else>
            <h1>Logging you in ...</h1>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                error: false,
                success: false
            }
        },
        created() {
            let code = this.$route.query.code;
            if (!code) {
                this.error = true;
                return
            }
            this.api.exchangeToken(code).then(resp => {
                if (!resp.ok) {
                    this.error = true
                } else {
                    this.success = true
                }
            }).catch(() => {
                this.error = true
            })
        },
        computed: {
            api() {
                return this.$store.state.api
            }
        }
    }
</script>