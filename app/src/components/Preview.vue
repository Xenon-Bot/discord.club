<template>
    <div>
        <div class="message">
            <div class="header">
                <img v-bind:src="avatarUrl" alt="Avatar" class="avatar">
                <h1 class="username">{{ data.username ? data.username : 'Captain Hook'}}</h1>
                <span class="bot-badge">BOT</span>
                <span class="timestamp">Today at {{messageTime}}</span>
            </div>
            <div v-if="data.content !== undefined && data.content !== null && data.content.trim() !== ''"
                 class="content">{{data.content}}
            </div>
            <!-- TODO: Attachments -->
            <div v-for="(embed, i) in data.embeds" v-bind:key="i" class="embeds">
                <div class="embed" v-bind:style="{borderColor: '#' + embed.color.toString(16)}">
                    <div class="embed-body">
                        <div class="author" v-if="embed.author && embed.author.name">
                            <img v-if="embed.author.icon_url" v-bind:src="embed.author.icon_url" alt="Icon"
                                 class="author-icon">
                            <a v-if="embed.author.url" v-bind:href="embed.author.url" class="author-name"
                               target="_blank">{{ embed.author.name }}</a>
                            <span v-else class="author-name">{{ embed.author.name }}</span>
                        </div>
                        <span class="title" v-if="embed.title">
                        <a class="title-content" v-if="embed.url" v-bind:href="embed.url" target="_blank">{{embed.title}}</a>
                        <span class="title-content" v-else>{{embed.title}}</span>
                    </span>
                        <div class="description">
                            <div class="description-content" v-if="embed.description">{{embed.description}}</div>
                        </div>
                        <div class="fields" v-if="embed.fields">
                            <!-- TODO: Field inline -->
                            <div v-for="(field, i) in embed.fields" v-bind:key="i" class="field"
                                 style="grid-column: 1 / 13;">
                                <div class="field-name">
                                    <div class="field-name-content">{{field.name}}</div>
                                </div>
                                <div class="field-value">
                                    <div class="field-value-content">{{field.value}}</div>
                                </div>
                            </div>
                        </div>
                        <img v-if="embed.image && embed.image.url" v-bind:src="embed.image.url" alt="image"
                             class="image">
                        <div class="footer"
                             v-if="embed.timestamp || (embed.footer && (embed.footer.text || embed.footer.icon_url))">
                            <img v-if="embed.footer.icon_url" v-bind:src="embed.footer.icon_url" alt="Icon"
                                 class="footer-icon">
                            <span class="footer-text">
                            {{embed.footer.text}}
                            <span v-if="embed.timestamp">
                                <span class="footer-separator" v-if="embed.timestamp && embed.footer.text">•</span>
                                <span>{{new Date(embed.timestamp).toLocaleDateString()}}</span>
                            </span>
                        </span>
                        </div>
                        <div class="thumbnail" v-if="embed.thumbnail && embed.thumbnail.url">
                            <img v-bind:src="embed.thumbnail.url" alt="thumbnail">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        props: ['data'],
        computed: {
            avatarUrl() {
                if (this.data.avatar_url) {
                    return this.data.avatar_url
                }
                return 'https://cdn.discordapp.com/embed/avatars/0.png'
            },
            messageTime() {
                return new Date().toLocaleTimeString().replace(/(.*)\D\d+/, '$1');
            },
        },
    }
</script>

<style scoped lang="scss">
    .message {
        line-height: 1;
        color: rgb(220, 221, 222);
        font-family: Whitney, Helvetica Neue, Helvetica, Arial, sans-serif;
        font-size: 16px;
        text-rendering: optimizelegibility;

        padding: 0.125rem 16px 0.125rem 4.5rem;
        min-height: 2.75rem;

        .header {
            position: relative;
            margin-left: -4.5rem;
            padding-left: 4.5rem;
            margin-bottom: 3px;

            .avatar {
                height: 2.5rem;
                width: 2.5rem;
                position: absolute;
                left: 0px;
                top: 0.125rem;
                margin: 0px 1rem;
                border-radius: 50%;
                object-fit: cover;
                cursor: pointer;
            }

            .username {
                display: inline;
                vertical-align: baseline;
                margin: 0px 0.25rem 0px 0px;
                color: rgb(255, 255, 255);
                font-size: 1rem;
                font-weight: 500;
                line-height: 1.375rem;
                overflow-wrap: break-word;
                cursor: pointer;
            }

            .bot-badge {
                position: relative;
                top: -0.1rem;
                min-height: 1.275em;
                max-height: 1.275em;
                margin: 0.075em 0.25rem 0px 0px;
                padding: 0.071875rem 0.275rem;
                border-radius: 3px;
                background: rgb(114, 137, 218) none repeat scroll 0% 0%;
                color: rgb(255, 255, 255);
                font-size: 0.625em;
                font-weight: 500;
                line-height: 1.3;
                vertical-align: baseline;
            }

            .timestamp {
                display: inline-block;
                height: 1.25rem;
                color: rgb(114, 118, 125);
                margin-left: 0.25rem;
                font-size: 0.75rem;
                font-weight: 500;
                line-height: 1.375rem;
                vertical-align: baseline;
            }
        }

        .content {
            white-space: pre-wrap;
            overflow-wrap: break-word;
            line-height: 1.375;
            margin-bottom: 10px;
        }

        .embeds {
            margin-top: 5px;
            display: grid;
            grid-auto-flow: row;
            row-gap: 0.25rem;
            padding: 0.125rem 0px;
            text-indent: 0px;

            .embed {
                place-self: start;
                text-align: left;
                max-width: 520px;
                display: grid;
                background: rgb(47, 49, 54) none repeat scroll 0% 0%;
                border-radius: 4px;
                border-left: 4px solid rgb(32, 34, 37);

                .embed-body {
                    padding: 0.5rem 1rem 1rem 0.75rem;
                    display: inline-grid;
                    grid-template-columns: auto;
                    grid-template-rows: auto;

                    .author {
                        min-width: 0px;
                        display: flex;
                        -moz-box-align: center;
                        align-items: center;
                        grid-column: 1 / 2;
                        margin: 8px 0px 0px;

                        .author-icon {
                            height: 24px;
                            width: 24px;
                            margin: 0px 8px 0px 0px;
                            object-fit: contain;
                            border-radius: 50%;
                        }

                        .author-name {
                            font-size: 0.875rem;
                            font-weight: 500;
                            color: rgb(255, 255, 255);
                            white-space: pre-wrap;
                            display: inline-block;
                        }
                    }

                    .title {
                        min-width: 0px;
                        display: inline-block;
                        margin: 8px 0px 0px;
                        grid-column: 1 / 2;

                        a {
                            color: rgb(0, 176, 244);
                        }

                        span {
                            color: rgb(255, 255, 255);
                        }

                        .title-content {
                            font-size: 1rem;
                            font-weight: 600;
                            white-space: pre-wrap;
                            overflow-wrap: break-word;
                            line-height: 1.375;
                        }
                    }

                    .description {
                        min-width: 0px;
                        margin: 8px 0px 0px;
                        grid-column: 1 / 2;

                        .description-content {
                            font-size: 0.875rem;
                            color: rgb(220, 221, 222);
                            line-height: 1.125rem;
                            white-space: pre-line;
                            overflow-wrap: break-word;
                        }
                    }

                    .fields {
                        min-width: 0px;
                        margin: 8px 0px 0px;
                        display: grid;
                        grid-column: 1 / 2;
                        gap: 8px;

                        .field {
                            min-width: 0px;
                            font-size: 0.875rem;
                            line-height: 1.125rem;

                            .field-name {
                                min-width: 0px;
                                margin: 0px 0px 1px;
                                font-size: 0.875rem;
                                font-weight: 600;
                                color: rgb(255, 255, 255);

                                .field-name-content {
                                    white-space: pre-wrap;
                                    overflow-wrap: break-word;
                                    line-height: 1.375;
                                }
                            }

                            .field-value {
                                min-width: 0;

                                .field-value-content {
                                    font-size: 0.875rem;
                                    line-height: 1.125rem;
                                    color: rgb(220, 221, 222);
                                    white-space: pre-line;
                                }
                            }
                        }
                    }

                    .image {
                        min-width: 0px;
                        max-width: 400px;
                        max-height: 300px;
                        margin: 16px 0px 0px;
                        border-radius: 4px;
                        cursor: pointer;
                        grid-column: 1 / 3;
                    }

                    .footer {
                        min-width: 0px;
                        margin: 8px 0px 0px;
                        display: flex;
                        -moz-box-align: center;
                        align-items: center;
                        grid-area: auto / 1 / auto / 3;

                        .footer-icon {
                            height: 20px;
                            width: 20px;
                            margin: 0px 8px 0px 0px;
                            object-fit: contain;
                            border-radius: 50%;
                        }

                        .footer-text {
                            font-size: 0.75rem;
                            font-weight: 500;
                            color: rgb(220, 221, 222);
                            line-height: 1rem;
                            white-space: break-spaces;

                            .footer-separator {
                                display: inline-block;
                                margin: 0px 4px;
                            }
                        }
                    }

                    .thumbnail {
                        margin: 8px 0px 0px 16px;
                        grid-area: 1 / 2 / 8 / 3;
                        justify-self: end;
                        cursor: pointer;

                        img {
                            max-width: 80px;
                            max-height: 80px;
                            border-radius: 4px;
                        }
                    }
                }
            }
        }
    }
</style>