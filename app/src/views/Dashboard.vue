<template>
    <div class="dashboard">
        <nav class="topbar navbar navbar-expand-lg navbar-dark bg-darker">
        <span class="navbar-brand">
          <span class="sidebar-trigger h4 align-middle ml-2 mr-2 c-pointer" v-on:click="sidebarShow = !sidebarShow">
            <i class="fas fa-bars"/>
          </span>
          {{ currentRouteName }}
        </span>
            <div class="navbar-nav ml-auto">
                <router-link to="/">
                    <button class="btn btn-lg btn-outline-primary my-2 my-sm-0">
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
            </div>
        </div>
        <div class="main" v-on:click="sidebarShow = false">
            <div class="container-fluid pt-4 px-2 p-lg-4">
                <router-view/>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Dashboard',
        data() {
            return {
                sidebarShow: false
            }
        },
        computed: {
            currentRouteName() {
                return this.$route.name;
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
</style>
