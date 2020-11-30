<template>
    <div class="home">
        <div class="main">
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                <button class="navbar-toggler" type="button" data-toggle="collapse"
                        data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                        aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <div class="container">
                        <ul class="navbar-nav mr-auto">
                            <li class="nav-item">
                                <a class="nav-link mr-3 text-light" href="/support">Support</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link text-light" href="/invite">Invite Bot</a>
                            </li>
                        </ul>
                        <div class="navbar-nav">
                            <router-link to="/dashboard">
                                <button class="btn btn-lg btn-outline-primary my-2 my-sm-0">
                                    Dashboard
                                    <i class="fas fa-angle-double-right ml-1"></i>
                                </button>
                            </router-link>
                        </div>
                    </div>
                </div>
            </nav>
            <div class="footer-push"></div>
        </div>
        <div class="footer bg-darker">
            <div class="container pt-5">
                <div class="row">
                    <div class="col-12 col-md-6 mb-2">
                        <h4>Discord.Club</h4>
                        <h5 class="lead">Copyright © 2020 Merlin Fuchs</h5>
                    </div>
                    <div class="col-6 col-md-3 col-sm-6 mb-3">
                        <ul class="nav flex-column">
                            <li class="nav-item">
                                <a href="/discord" class="nav-link text-light p-1">Discord</a>
                            </li>
                            <li class="nav-item">
                                <a href="mailto:contact@discord.club" class="nav-link text-light p-1">Email</a>
                            </li>
                        </ul>
                    </div>
                    <div class="col-6 col-md-3 col-sm-6 mb-3">
                        <ul class="nav flex-column">
                            <li class="nav-item">
                                <a href="/legal/privacy" class="nav-link text-light p-1">Privacy Policy</a>
                            </li>
                            <li class="nav-item">
                                <a href="/legal/cookies" class="nav-link text-light p-1">Cookie Policy</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Home',
        components: {}
    }
</script>

<style scoped lang="scss">
    $footer-height: 200px;
    .main {
        min-height: 100vh;
        margin-bottom: -$footer-height;
    }

    .footer-push {
        height: $footer-height;
    }

    .footer {
        min-height: $footer-height;
    }

    .nav-item {
        font-size: 1.3rem;
    }
</style>
