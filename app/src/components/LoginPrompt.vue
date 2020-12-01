<template>
    <div class="card bg-darker">
        <div class="card-header">
            <h4 class="card-title">Please Login</h4>
            <h6 class="card-subtitle text-muted">This part of the site can only be accessed by authenticated users</h6>
        </div>
        <div class="card-body text-center">
            <a href="/login" target="_blank" class="py-5">
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