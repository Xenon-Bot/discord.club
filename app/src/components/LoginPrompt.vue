<template>
    <div class="card bg-darker">
        <div class="card-header">
            <h4 class="card-title">Please Login</h4>
            <h6 class="card-subtitle text-muted">This part of the site can only be accessed by authenticated users. Click on the discord logo below to login.</h6>
        </div>
        <div class="card-body text-center">
            <a href="https://discord.com/api/oauth2/authorize?client_id=410138706490425344&redirect_uri=https%3A%2F%2Fdiscord.club%2Fcallback&response_type=code&scope=identify"
               class="py-5">
                <img src="@/assets/discord.png" alt="" class="discord-logo">
            </a>
        </div>
    </div>
</template>
<style scoped lang="scss">
    .discord-logo:hover {
        transform: rotate(360deg);
        transition: transform 0.5s;
    }
</style>