<template>
    <div class="container">
        <div class="text-center header">
            <h1 class="d-none">Discord.Club - Embed Generator</h1>
            <h2 class="mb-5">Bring your discord to the next level!</h2>
            <router-link class="btn btn-primary btn-lg mr-3" to="/dashboard">Start Now</router-link>
            <a href="/discord" class="btn btn-dark btn-lg">Support</a>
        </div>
        <div class="features">
            <div class="feature p-3 p-md-5 bg-primary text-dark">
                <div class="row">
                    <div class="col-12 col-md-6 col-lg-5 left">
                        <img src="@/assets/editor.png" alt="">
                    </div>
                    <div class="col-12 col-md-6 colg-lg-7 right pl-md-5">
                        <div class="push d-block d-md-none"></div>
                        <h5 class="font-weight-bold">Full Webhook Capabilities</h5>
                        <p>
                            Plain text messages were yesterday. Start using discord.club and take advantage of
                            all the features discord webhooks provide with one mouse click: Up to 10 embeds,
                            file attachments, hyperlinks and more!
                        </p>
                    </div>
                </div>
            </div>
            <div class="feature p-3 p-md-5 bg-primary text-dark">
                <div class="row">
                    <div class="col-12 col-md-6 order-md-6 col-lg-5 right">
                        <img src="@/assets/preview.png" alt="">
                    </div>
                    <div class="col-12 col-md-6 order-md-0 col-lg-7 left pl-md-5">
                        <div class="push d-block d-md-none"></div>
                        <h5 class="font-weight-bold">Live Preview</h5>
                        <p>
                            Wonder how your messages will look like in discord? Discord.club provides an
                            accurate live preview of your message including embeds, files and markdown!
                        </p>
                    </div>
                </div>
            </div>
            <div class="feature p-3 p-md-5 bg-primary text-dark">
                <div class="row">
                    <div class="col-12 col-md-6 col-lg-5 left">
                        <img src="@/assets/messages.png" alt="">
                    </div>
                    <div class="col-12 col-md-6 colg-lg-7 right pl-md-5">
                        <div class="push d-block d-md-none"></div>
                        <h5 class="font-weight-bold">Store Messages</h5>
                        <p>
                            Never lose any of your previously generated messages. Save your messages on our
                            servers and continue editing when and wherever you are.
                        </p>
                    </div>
                </div>
            </div>
            <div class="feature p-3 p-md-5 bg-primary text-dark">
                <div class="row">
                    <div class="col-12 col-md-6 order-md-6 col-lg-5 right">
                        <img src="@/assets/editor.png" alt=""
                             style="filter: blur(5px);-webkit-filter: blur(5px); overflow: hidden">
                    </div>
                    <div class="col-12 col-md-6 order-md-0 col-lg-7 left pl-md-5">
                        <div class="push d-block d-md-none"></div>
                        <h5 class="font-weight-bold">Automated Messages</h5>
                        <p>
                            Tired of sending the messages yourself? Use discord.club to schedule your messages
                            to be sent at a specific time or respond to commands with your custom messages.
                            You can even track the status of your favorite streamer and send a message when they
                            are live!
                        </p>
                        <span class="h4"><span class="badge badge-secondary">Coming Soon</span></span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Index',
        components: {}
    }
</script>

<style scoped lang="scss">
    .header {
        margin-top: 175px;

        h2 {
            font-size: 3.3em;
            font-weight: bold;
        }
    }

    .features {
        margin-top: 275px;

        .feature {
            width: 100%;
            margin-bottom: 150px;
            border-radius: 20px;

            img {
                border-radius: 10px;
                width: 100%;
                overflow: hidden;
                margin-bottom: -30%;
                margin-top: -40%;
                transition: transform 0.2s;
            }

            .left {
                img {
                    transform: perspective(1000px) rotateX(10deg) rotateY(10deg) rotate(-5deg);
                    box-shadow: -50px 50px 100px -25px rgba(9, 9, 14, .5);

                    &:hover {
                        transform: none;
                    }
                }
            }

            .right {
                img {
                    transform: perspective(1000px) rotateX(10deg) rotateY(-10deg) rotate(5deg);
                    box-shadow: 50px 50px 100px -25px rgba(9, 9, 14, .5);

                    &:hover {
                        transform: none;
                    }
                }
            }

            .push {
                margin-top: 45%;
            }
        }
    }
</style>
