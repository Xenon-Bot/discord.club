<template>
    <div class="quick" v-on:paste="addFileFromClipboard">
        <div class="row">
            <div class="col-12 col-xl-6 mb-5">
                <h4 class="ml-2 mb-3">Webhook</h4>
                <div class="card border-0 tex-light mb-4 bg-darker">
                    <div class="card-body mb-0">
                        <div class="form-row mb-2">
                            <div class="col-12 mb-4">
                                <label>Webhook URL</label>
                                <input v-model.trim.lazy="webhookUrl" type="url" class="form-control"
                                       placeholder="https://discord.com/api/webhooks/423157583646294017/nsFEJfuNKVBRcKcgj0JX3TygdvhX-ItEJhrWVWadw7shUXXuIRwsJHUS_XbDDSA_ILKN">
                            </div>
                            <div class="col-12 mb-4">
                                <label>Message ID or URL
                                    <span class="ml-1 hover-tooltip" title="yeet">
                                    <i class="fas fa-question hover-tooltip-trigger"/>
                                    <span class="hover-tooltip-content bg-dark py-2 px-3 rounded">
                                        If you want to edit an existing message, you can paste the message link or id here.
                                        The author of the message must be a webhook. 
                                    </span>
                                </span>
                                </label>
                                <input v-model.trim.lazy="messageUrl" type="text" class="form-control"
                                       placeholder="https://discord.com/channels/410488579140354049/633228954064650250/781981855808487477">
                            </div>
                        </div>
                        <button class="btn btn-outline-primary float-right" v-on:click="sendMessage"
                                v-bind:class="{disabled: !this.webhookUrl}">
                            <span v-if="messageId">Edit</span>
                            <span v-else>Send</span>
                            Message
                        </button>
                    </div>
                </div>
                <h4 class="ml-2 mb-3">Message</h4>
                <div class="card border-0 tex-light mb-4 bg-darker">
                    <div class="card-body">
                        <div class="form-row mb-2">
                            <div class="col-12 col-lg-6 mb-4">
                                <label>Username</label>
                                <span class="text-muted ml-2 char-counter">{{ webhookUsername ? webhookUsername.length : 0 }} / 80</span>
                                <input v-model.trim="webhookUsername" type="text" class="form-control"
                                       placeholder="Captain Hook" maxlength="80">
                            </div>
                            <div class="col-12 col-lg-6">
                                <label>Avatar URL
                                    <span class="ml-1 hover-tooltip" title="yeet">
                                        <i class="fas fa-question hover-tooltip-trigger"/>
                                        <span class="hover-tooltip-content bg-dark py-2 px-3 rounded">
                                            Image URLs must resolve to a valid image and respond with the correct Content-Type header.
                                            URLs ending with .png, .webp, .jpg or .jpeg are in most cases safe to use.
                                        </span>
                                    </span>
                                </label>
                                <input v-model.trim="webhookAvatarUrl" type="url" class="form-control"
                                       placeholder="https://i.imgur.com/yed5Zfk.png">
                            </div>
                            <div class="col-12 mb-4">
                                <label>Content</label>
                                <span class="text-muted ml-2 char-counter">{{ content ? content.length : 0 }} / 2000</span>
                                <div class="form-check float-right">
                                    <input v-model.trim="tts" type="checkbox" class="form-check-input">
                                    <label class="form-check-label">TTS</label>
                                </div>
                                <textarea v-model="content" rows="5" class="form-control" placeholder="I like webhooks"
                                          maxlength="2000"/>
                            </div>
                            <div class="col-12">
                                <label>Files</label>
                                <span class="text-muted ml-2 char-counter">Max. 8 MB</span>
                                <div class="row mb-2 m-0">
                                <span v-for="(file, i) in files" v-bind:key="i"
                                      class="px-2 py-1 m-1 bg-dark col-auto rounded">
                                    <label class="mr-2 d-inline">{{file.name}}</label>
                                    <span class="c-pointer d-line" v-on:click="deleteFile(i)"><i
                                            class="fas fa-minus"/></span>
                                </span>
                                </div>
                                <input type="file" class="btn btn-sm btn-outline-light mr-2"
                                       v-on:change="addFileFromInput">
                                <div class="btn btn-sm btn-outline-light" v-on:click="clearFiles">
                                    <i class="fas fa-trash"/>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <h4 class="ml-2 mb-3">Embeds <span
                        class="text-muted ml-2 char-counter h6">{{ embeds.length }} / 10</span></h4>
                <div class="mb-5">
                    <div v-for="(embed, e) in embeds" v-bind:key="e" class="card tex-light mb-3 bg-darker"
                         v-bind:style="{borderLeft: '5px solid' + embed.color}">
                        <div class="card-body">
                            <div class="float-right" style="font-size: 1.1rem">
                                <span class="mr-3 c-pointer" v-if="e !== 0" v-on:click="moveEmbedUp(e)"><i
                                        class="fas fa-chevron-up"/></span>
                                <span class="mr-3 c-pointer" v-if="e !== embeds.length - 1"
                                      v-on:click="moveEmbedDown(e)"><i class="fas fa-chevron-down"/></span>
                                <span class="mr-3 c-pointer" v-if="embeds.length < 10" v-on:click="cloneEmbed(e)"><i
                                        class="far fa-copy"/></span>
                                <span class="mr-3 c-pointer" v-on:click="deleteEmbed(e)"><i
                                        class="fas fa-minus"/></span>
                            </div>
                            <h5 data-toggle="collapse" v-bind:data-target="'#embed' + e" role="button"
                                class="overflow-auto text-nowrap">
                                Embed {{ e + 1 }}
                                <span v-if="embed.title" class="text-muted">- {{ embed.title.substring(0, 15) }}</span>
                            </h5>
                            <div class="collapse mt-3" v-bind:id="'embed' + e">
                                <div class="form-row">
                                    <div class="col-12 mb-4">
                                        <label>Author</label>
                                        <span class="text-muted ml-2 char-counter">{{ embed.authorName ? embed.authorName.length : 0 }} / 256</span>
                                        <input v-model.trim="embed.authorName" type="text" class="form-control"
                                               placeholder="Doctor Who" maxlength="256">
                                    </div>
                                    <div class="col-12 col-lg-6 mb-4">
                                        <label>Author URL</label>
                                        <input v-model.trim="embed.authorUrl" type="url" class="form-control"
                                               placeholder="https://discord.club">
                                    </div>
                                    <div class="col-12 col-lg-6 mb-4">
                                        <label>Author Icon URL
                                            <span class="ml-1 hover-tooltip" title="yeet">
                                        <i class="fas fa-question hover-tooltip-trigger"></i>
                                        <span class="hover-tooltip-content bg-dark py-2 px-3 rounded">
                                            Image URLs must resolve to a valid image and respond with the correct Content-Type header.
                                            URLs ending with .png, .webp, .jpg or .jpeg are in most cases safe to use.
                                        </span>
                                    </span>
                                        </label>
                                        <input v-model.trim="embed.authorIconUrl" type="url" class="form-control"
                                               placeholder="https://i.imgur.com/yed5Zfk.png">
                                    </div>
                                </div>
                                <div class="form-row">
                                    <div class="col-12 mb-4">
                                        <label>Title</label>
                                        <span class="text-muted ml-2 char-counter">{{ embed.title ? embed.title.length : 0 }} / 256</span>
                                        <input v-model.trim="embed.title" type="text" class="form-control"
                                               placeholder="My Embed" maxlength="256">
                                    </div>
                                    <div class="col-12 mb-4">
                                        <label>Description</label>
                                        <span class="text-muted ml-2 char-counter">{{ embed.description ? embed.description.length : 0 }} / 2048</span>
                                        <textarea v-model="embed.description" class="form-control"
                                                  placeholder="My first template" rows="5" maxlength="2048"/>
                                    </div>
                                    <div class="col-12 col-lg-6 mb-4">
                                        <label>URL</label>
                                        <input v-model.trim="embed.url" type="url" class="form-control"
                                               placeholder="https://discord.club">
                                    </div>
                                    <div class="col-12 col-lg-6 mb-4">
                                        <label>Color</label>
                                        <!-- TODO: Replace with third-party color picker -->
                                        <input v-model="embed.color" type="color" class="form-control">
                                    </div>
                                </div>
                                <div class="form-row">
                                    <div class="col-12 col-lg-6 mb-4">
                                        <label>Image URL
                                            <span class="ml-1 hover-tooltip" title="yeet">
                                            <i class="fas fa-question hover-tooltip-trigger"/>
                                            <span class="hover-tooltip-content bg-dark py-2 px-3 rounded">
                                                Image URLs must resolve to a valid image and respond with the correct Content-Type header.
                                                URLs ending with .png, .webp, .jpg or .jpeg are in most cases safe to use.
                                            </span>
                                        </span>
                                        </label>
                                        <input v-model.trim="embed.imageUrl" type="url" class="form-control"
                                               placeholder="https://i.imgur.com/yed5Zfk.png">
                                    </div>
                                    <div class="col-12 col-lg-6 mb-4">
                                        <label>Thumbnail URL
                                            <span class="ml-1 hover-tooltip" title="yeet">
                                            <i class="fas fa-question hover-tooltip-trigger"/>
                                            <span class="hover-tooltip-content bg-dark py-2 px-3 rounded">
                                                Image URLs must resolve to a valid image and respond with the correct Content-Type header.
                                                URLs ending with .png, .webp, .jpg or .jpeg are in most cases safe to use.
                                            </span>
                                        </span>
                                        </label>
                                        <input v-model.trim="embed.thumbnailUrl" type="url" class="form-control"
                                               placeholder="https://i.imgur.com/yed5Zfk.png">
                                    </div>
                                </div>
                                <div class="form-row">
                                    <div class="col-12 mb-4">
                                        <label>Footer Text</label>
                                        <span class="text-muted ml-2 char-counter">{{ embed.footerText ? embed.footerText.length : 0 }} / 256</span>
                                        <input v-model.trim="embed.footerText" type="text" class="form-control"
                                               placeholder="this is the end" maxlength="256">
                                    </div>
                                    <div class="col-12 col-lg-6 mb-4">
                                        <label>Timestamp</label>
                                        <div class="form-row">
                                            <div class="col">
                                                <datetime v-model.trim="embed.timestamp" type="datetime"
                                                          input-class="form-control"/>
                                            </div>
                                            <div class="col-auto">
                                                <button class="btn btn-outline-light"
                                                        v-on:click="embed.timestamp = null">
                                                    <i class="fas fa-eraser"/>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-12 col-lg-6 mb-4">
                                        <label>Footer Icon URL
                                            <span class="ml-1 hover-tooltip" title="yeet">
                                            <i class="fas fa-question hover-tooltip-trigger"/>
                                            <span class="hover-tooltip-content bg-dark py-2 px-3 rounded">
                                                Image URLs must resolve to a valid image and respond with the correct Content-Type header.
                                                URLs ending with .png, .webp, .jpg or .jpeg are in most cases safe to use.
                                            </span>
                                        </span>
                                        </label>
                                        <input v-model.trim="embed.footerIconUrl" type="url" class="form-control"
                                               placeholder="https://i.imgur.com/yed5Zfk.png">
                                    </div>
                                </div>
                                <h5>Fields <span class="text-muted ml-2 char-counter">{{ embed.fields ? embed.fields.length : 0 }} / 10</span>
                                </h5>
                                <div v-for="(field, f) in embed.fields" v-bind:key="f">
                                    <label>Field {{ f + 1 }}</label>
                                    <span class="text-muted ml-2 char-counter">{{ field.name ? field.name.length : 0 }} / 256</span>
                                    <span class="text-muted ml-2 char-counter">{{ field.value ? field.value.length : 0 }} / 1024</span>
                                    <span class="c-pointer float-right" v-on:click="deleteField(e, f)"><i
                                            class="fas fa-minus"/></span>
                                    <div class="form-row mb-3">
                                        <div class="col-8 col-sm-10 mb-3">
                                            <input v-model.trim="field.name" type="text" class="form-control"
                                                   placeholder="Name" maxlength="256">
                                        </div>
                                        <div class="col-4 col-sm-2 mb-3">
                                            <div class="form-check pt-2">
                                                <input v-model.trim="field.inline" type="checkbox"
                                                       class="form-check-input">
                                                <label class="form-check-label">Inline</label>
                                            </div>
                                        </div>
                                        <div class="col-12">
                                            <textarea v-model.trim="field.value" rows="2" class="form-control"
                                                      placeholder="Value" maxlength="1024"/>
                                        </div>
                                    </div>
                                </div>
                                <div class="btn btn-sm btn-outline-light mr-2" v-on:click="clearFields(e)">
                                    <i class="fas fa-trash"/>
                                </div>
                                <div class="btn btn-sm btn-outline-light" v-on:click="addField(e)"
                                     v-bind:class="{disabled: embed.fields ? embed.fields.length >= 10 : false}">
                                    <i class="fas fa-plus"/>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="btn btn-sm btn-outline-secondary mr-2" v-on:click="clearEmbeds">
                        <i class="fas fa-trash"/>
                    </div>
                    <div class="btn btn-sm btn-outline-primary" v-on:click="addEmbed"
                         v-bind:class="{disabled: embeds.length >= 10}">
                        <i class="fas fa-plus"/>
                    </div>
                </div>
            </div>
            <div class="col-12 col-xl-6">
                <h4 class="ml-2 mb-3">Preview</h4>
                <div class="card preview mb-5 bg-discordbg">
                    <div class="card-body px-1 py-3">
                        <preview v-bind:data="getJSON()"/>
                    </div>
                </div>
                <h4 class="ml-2 mb-3">JSON Code</h4>
                <div class="card bg-darker mb-5">
                    <div class="card-body px-3 py-3">
                        <textarea v-model.lazy="jsonCode" class="form-control mb-2" rows="10"/>
                        <span class="text-danger">{{ jsonError }}</span>
                        <button class="btn btn-outline-secondary float-right" v-on:click="onSave">
                            Save Message
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Preview from './Preview.vue'
    import {Datetime} from 'vue-datetime'
    import 'vue-datetime/dist/vue-datetime.css'

    export default {
        name: 'Editor',
        components: {Preview, Datetime},
        props: ['onSave'],
        data() {
            return {
                webhookId: "",
                webhookToken: "",
                messageId: "",
                webhookUsername: "",
                webhookAvatarUrl: "",
                content: "",
                tts: undefined,
                files: [],
                embeds: [],
                jsonError: ""
            }
        },
        created() {
            const lastData = localStorage.getItem("lastData")
            if (lastData) {
                this.setJSON(JSON.parse(lastData));
            }
        },
        methods: {
            getJSON() {
                let embeds = []
                for (let embed of this.embeds) {
                    embeds.push({
                        title: embed.title,
                        color: embed.color ? parseInt(embed.color.substring(1), 16) : undefined,
                        description: embed.description,
                        timestamp: embed.timestamp,
                        url: embed.url,
                        author: {
                            name: embed.authorName,
                            url: embed.authorUrl,
                            icon_url: embed.authorIconUrl
                        },
                        image: {
                            url: embed.imageUrl
                        },
                        thumbnail: {
                            url: embed.thumbnailUrl
                        },
                        footer: {
                            text: embed.footerText,
                            icon_url: embed.footerIconUrl
                        },
                        fields: embed.fields
                    });
                }

                const data = {
                    username: this.webhookUsername,
                    avatar_url: this.webhookAvatarUrl,
                    content: this.content,
                    tts: this.tts,
                    embeds: embeds
                }
                localStorage.setItem("lastData", JSON.stringify(data))
                return data
            },
            setJSON(data) {
                let embeds = []
                if (data.embeds) {
                    for (let embed of data.embeds) {
                        let parsed = {
                            title: embed.title,
                            color: embed.color ? "#" + embed.color.toString(16) : "#000",
                            description: embed.description,
                            timestamp: embed.timestamp,
                            tts: embed.tts,
                            url: embed.url,
                            fields: embed.fields
                        }

                        if (embed.author) {
                            parsed.authorName = embed.author.name
                            parsed.authorUrl = embed.author.url
                            parsed.authorIconUrl = embed.author.icon_url
                        }

                        if (embed.image) {
                            parsed.imageUrl = embed.image.url
                        }

                        if (embed.thumbnail) {
                            parsed.thumbnailUrl = embed.thumbnail.url
                        }

                        if (embed.footer) {
                            parsed.footerText = embed.footer.text
                            parsed.footerIconUrl = embed.footer.icon_url
                        }

                        embeds.push(parsed);
                    }
                }

                this.webhookUsername = data.username;
                this.webhookAvatarUrl = data.avatar_url;
                this.content = data.content;
                this.embeds = embeds;
            },
            addEmbed() {
                if (this.embeds.length >= 10) {
                    return
                }
                this.embeds.push({color: "#000"})
            },
            clearEmbeds() {
                this.embeds = []
            },
            deleteEmbed(i) {
                this.embeds.splice(i, 1)
            },
            moveEmbedUp(i) {
                console.log(i)
                this.embeds.splice(i - 1, 0, this.embeds.splice(i, 1)[0])
            },
            moveEmbedDown(i) {
                this.embeds.splice(i + 1, 0, this.embeds.splice(i, 1)[0])
            },
            cloneEmbed(i) {
                if (this.embeds.length >= 10) {
                    return
                }
                this.embeds.splice(i + 1, 0, JSON.parse(JSON.stringify(this.embeds[i])))
            },
            addField(e) {
                let embed = this.embeds[e];
                if (!embed.fields) {
                    embed.fields = []
                }
                if (embed.fields.length >= 10) {
                    return
                }
                embed.fields.push({})
            },
            clearFields(e) {
                this.embeds[e].fields = []
            },
            deleteField(e, i) {
                let embed = this.embeds[e];
                if (embed.fields) {
                    embed.fields.splice(i, 1)
                }
            },
            sendMessage() {
                if (!this.webhookUrl) return
                if (this.messageId) {
                    // TODO: default content to " " to remove existing content
                    fetch(`${this.webhookUrl}/messages/${this.messageId}`, {
                        method: 'PATCH',
                        body: JSON.stringify(this.getJSON()),
                        headers: {'Content-Type': 'application/json'}
                    })
                        .then(resp => alert(resp.status))
                } else {
                    let data = new FormData()
                    data.append('payload_json', JSON.stringify(this.getJSON()))
                    for (let i in this.files) {
                        let file = this.files[i]
                        data.append(`file${i}`, new Blob([file.content]), file.name)
                    }

                    fetch(`${this.webhookUrl}?wait=true`, {
                        method: 'POST',
                        body: data
                    })
                        .then(resp => {
                            alert(resp.status)
                            return resp.json()
                        })
                        .then(data => this.messageId = data.id)
                }
            },
            addFile(file) {
                let reader = new FileReader()
                reader.readAsArrayBuffer(file)
                reader.onload = re => {
                    let nameParts = file.name.split(".")
                    let name = nameParts.slice(0, -1);
                    let extension = nameParts[nameParts.length - 1];
                    let existingNames = this.files.map(f => f.name)
                    while (existingNames.includes(`${name}.${extension}`)) {
                        name += "_"
                    }

                    this.files.push({
                        name: `${name}.${extension}`,
                        content: re.target.result
                    })
                }
            },
            addFileFromInput(e) {
                let file = e.target.files[0]
                e.target.value = null;
                if (file) {
                    this.addFile(file)
                }
            },
            addFileFromClipboard(e) {
                let file = e.clipboardData.files[0]
                if (file) {
                    this.addFile(file)
                }
            },
            deleteFile(i) {
                this.files.splice(i, 1)
            },
            clearFiles() {
                this.files = []
            }
        },
        computed: {
            jsonCode: {
                get() {
                    return JSON.stringify(this.getJSON(), null, 2)
                },
                set(newValue) {
                    let data;
                    try {
                        data = JSON.parse(newValue);
                    } catch (SyntaxError) {
                        this.jsonError = "Invalid JSON-Code, unable to apply it.";
                        return;
                    }
                    this.jsonError = "";
                    this.setJSON(data);
                }
            },
            messageUrl: {
                get() {
                    return this.messageId
                },
                set(newValue) {
                    const urlRegex = /https:\/\/(canary\.)?discord(app)?.com\/channels\/[0-9]+\/[0-9]+\/([0-9]+)\/?/i
                    let match = newValue.toString().match(urlRegex);
                    if (match) {
                        this.messageId = match[3]
                    } else if (newValue.match(/^[0-9]+$/)) {
                        this.messageId = newValue
                    } else {
                        this.messageId = null;
                    }

                    if (this.webhookUrl && this.messageId) {
                        console.log("fetch")
                        fetch(`${this.webhookUrl}/messages/${this.messageId}`, {
                            method: 'PATCH',
                            body: '{}',
                            headers: {'Content-Type': 'application/json'}
                        })
                            .then(resp => {
                                if (resp.status != 200) {
                                    alert("Invalid message")
                                }
                                return resp.json()
                            })
                            .then(data => {
                                // TODO: add warning and confirmation before overwriting
                                this.setJSON(data)
                            })
                    }
                }
            },
            webhookUrl: {
                get() {
                    if (this.webhookId && this.webhookToken) {
                        return `https://discord.com/api/v8/webhooks/${this.webhookId}/${this.webhookToken}`
                    }
                    return null
                },
                set(newValue) {
                    const urlRegex = /https:\/\/(canary\.)?discord(app)?.com\/(api\/(v[6-8]\/)?)?webhooks\/([0-9]+)\/(.+)\/?/i
                    let match = newValue.match(urlRegex);
                    if (match) {
                        this.webhookId = match[5]
                        this.webhookToken = match[6]
                        fetch(this.webhookUrl)
                            .then(resp => resp.json())
                            .then(data => this.webhookUsername = data.name)
                    } else {
                        this.webhookId = null
                        this.webhookToken = null
                    }
                }
            }
        }
    }
</script>

<style scoped lang="scss">
    .preview {
        box-shadow: 0 0 2px #212121;
    }

    .hover-tooltip {
        position: relative;

        &:hover {
            .hover-tooltip-content {
                display: block;
            }
        }

        .hover-tooltip-content {
            display: none;
            position: absolute;
            width: 250px;
            left: 0;
            bottom: 25px;
            z-index: 10;
            box-shadow: 0 0 2px black;
        }

        .hover-tooltip-trigger {
            cursor: pointer;
        }
    }

    .char-counter {
        font-style: italic;
        font-size: 0.8em;
    }
</style>
<style>
    .vdatetime-popup {
        background-color: black;
        color: white;
    }

    .vdatetime-calendar__month__day:hover > span > span {
        background: #eee;
        color: black;
    }
</style>