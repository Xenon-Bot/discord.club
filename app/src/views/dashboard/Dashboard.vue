<template>
    <div class="dashboard">
        <nav class="topbar navbar navbar-expand-lg navbar-dark bg-darker">
        <span class="navbar-brand">
          <span class="sidebar-trigger h4 align-middle ml-2 mr-2 c-pointer" v-on:click="sidebarShow = !sidebarShow">
            <i class="fas fa-bars"/>
          </span>
          {{ currentRouteName }}
        </span>
            <div class="navbar-nav ml-auto mr-0 mr-md-2">
                <router-link to="/">
                    <button class="btn btn-lg btn-outline-primary">
                        Home
                        <i class="fas fa-angle-double-left ml-1"/>
                    </button>
                </router-link>
            </div>
        </nav>
        <div class="sidebar bg-darker" v-bind:class="{show: sidebarShow}">
            <div class="links" v-on:click="sidebarShow = false">
                <router-link to="/dashboard" class="link">
                    <span class="icon"><i class="fas fa-rocket"/></span>
                    <span class="text">Quick Message</span>
                </router-link>
                <router-link to="/dashboard/messages" class="link">
                    <span class="icon"><i class="fas fa-envelope-open-text"/></span>
                    <span class="text">Messages</span>
                </router-link>
                <router-link to="/dashboard/triggers" class="link">
                    <span class="icon"><i class="fas fa-magic"/></span>
                    <span class="text">Triggers</span>
                </router-link>
                <router-link to="/dashboard/help" class="link">
                    <span class="icon"><i class="fas fa-book"/></span>
                    <span class="text">Help & FAQ</span>
                </router-link>
                <div class="link link-bottom c-pointer" v-on:click="logout" v-if="api.isAuthenticated()">
                    <span class="icon"><i class="fas fa-sign-out-alt"/></span>
                    <span class="text">Logout</span>
                </div>
            </div>
        </div>
        <div class="main" v-on:click="sidebarShow = false">
            <div class="container-fluid pt-4 px-2 p-lg-4">
                <transition name="fade">
                    <router-view/>
                </transition>
            </div>
        </div>
        <div class="modal fade" id="introModal" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-lg" role="document" style="max-height: 90vh">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title">Welcome!</h3>
                    </div>
                    <div class="modal-body" style="max-height: 70vh; overflow: auto">
                        <p class="intro-text">
                            As you might have noticed, a lot has changed here. The whole site was undergoing a complete
                            rewrite in the past weeks and this is the result. Beside a new design, the rewrite also
                            has a lot of new features.
                        </p>
                        <h4 class="mt-4">New Features</h4>
                        <ul class="intro-text">
                            <li>Complete Redesign</li>
                            <li>Up to 10 embeds per message</li>
                            <li>Support for files / attachments</li>
                            <li>Editing existing messages</li>
                            <li>Proper message preview</li>
                            <li>Saving and editing messages with custom names</li>
                            <li>Actually meaningful error responses</li>
                        </ul>
                        <h4 class="mt-4">Quick Start</h4>
                        <p class="intro-text">
                            A lot has changed so here are some tips to get you started if you are coming from the old
                            website:
                        </p>
                        <ul class="intro-text">
                            <li>
                                You can now add up to 10 embeds using the
                                <span class="btn btn-sm btn-outline-primary">
                                    <i class="fas fa-plus"/>
                                </span>
                                button.
                            </li>
                            <li>You can collapse and un-collapse each embed by clicking on their name</li>
                            <li>
                                You can save your message using the
                                <button class="btn btn-sm btn-outline-secondary">
                                    Save Message
                                </button>
                                button
                            </li>
                            <li>Editing a saved message is possible by clicking on "Messages" on the left side</li>
                            <li>
                                Sending a message can be done by pasting a Webhook URL into the input and clicking the
                                <button class="btn btn-sm btn-outline-primary">
                                    Send Message
                                </button>
                                button
                            </li>
                            <li>
                                Editing a previously sent message can be done by pasting the Message URL or ID into the
                                input below the Webhook URL and clicking on the
                                <button class="btn btn-sm btn-outline-secondary">
                                    Edit Message
                                </button>
                                button
                            </li>
                            <li>
                                Creating a webhook is no longer possible directly over the website. You need to go to
                                the channel settings in discord and click on "Integrations" or "Webhooks" (depending on
                                your device) <br>
                                If you are using the mobile app, you can also use the <a href="/invite">discord bot</a>
                                to create a webhook: <code>&gt;webhook</code>
                            </li>
                        </ul>
                        <h4 class="mt-4">Migrating</h4>
                        <p class="intro-text">
                            You can easily migrate your previously saved embeds from the old website to the new one
                            until the 31th of January:
                        </p>
                        <ul class="intro-text">
                            <li>Go to <a href="https://old.discord.club" target="_blank">https://old.discord.club</a>
                            </li>
                            <li>Login with your discord account and select one of your previously saved embeds</li>
                            <li>Copy the JSON-Code on the old site and paste it on the new one.</li>
                            <li>Click "Save Message" on the new site and give the message a name. (You might need to
                                login)
                            </li>
                        </ul>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal" v-on:click="introClose">
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import $ from 'jquery'

    export default {
        name: 'Dashboard',
        data() {
            return {
                sidebarShow: false
            }
        },
        mounted() {
            const hasDoneIntro = localStorage.getItem("intro")
            if (!hasDoneIntro) {
                $('#introModal').modal({backdrop: 'static'})
            }
        },
        computed: {
            currentRouteName() {
                return this.$route.name;
            },
            api() {
                return this.$store.state.api
            }
        },
        methods: {
            logout() {
                this.api.deleteToken()
                window.location.replace("/")
            },
            introClose() {
                localStorage.setItem("intro", "true")
            }
        }
    }
</script>

<style scoped lang="scss">
    $sidebar-width: 250px;
    $topbar-height: 75px;
    $sidebar-collapse-at: 1200px;

    .sidebar {
        margin-top: $topbar-height;
        width: $sidebar-width;
        position: fixed;
        height: 100vh;
        top: 0;
        left: 0;
        padding-left: 25px;
        box-shadow: -10px 0px 22px black;
        z-index: 9;
        transition: left 0.3s;

        @media screen and (max-width: $sidebar-collapse-at) {
            left: -$sidebar-width;

            &.show {
                left: 0;
            }
        }

        .links {
            margin-top: 25px;
            height: 100%;
            position: relative;

            .link {
                font-size: 1.2rem;
                margin-bottom: 20px;
                display: block;
                color: white;
                text-decoration: none;

                .icon {
                    font-size: 1.4rem;
                }

                .text {
                    padding-left: 15px;
                }
            }

            .link-bottom {
                position: absolute;
                bottom: 100px;
            }
        }
    }

    .topbar {
        height: $topbar-height;
        box-shadow: 0px -10px 22px black;
        width: 100vw;
        position: fixed;
        top: 0;
        z-index: 10;

        .sidebar-trigger {
            display: none;
        }

        @media screen and (max-width: $sidebar-collapse-at) {
            .sidebar-trigger {
                display: inline;
            }
        }
    }

    .main {
        margin-top: $topbar-height;
        margin-left: $sidebar-width;
        transition: margin-left 0.3s;

        @media screen and (max-width: $sidebar-collapse-at) {
            margin-left: 0;
        }
    }

    .intro-text {
        font-size: 1.2em;

        li {
            margin-bottom: 0.3em;
        }
    }
</style>
