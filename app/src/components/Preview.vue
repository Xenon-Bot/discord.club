<template>
    <div>
        <div class="message">
            <div class="header">
                <img v-bind:src="avatarUrl" alt="Avatar" class="avatar">
                <h1 class="username">{{ json.username ? json.username : 'Captain Hook'}}</h1>
                <span class="bot-badge">BOT</span>
                <span class="timestamp">Today at {{messageTime}}</span>
            </div>
            <div v-if="json.content !== undefined && json.content !== null && json.content.trim() !== ''"
                 class="content">
                <markdown-highlight :text="json.content"/>
            </div>
            <div class="embeds">
                <div v-for="(file, i) in files" v-bind:key="i" class="file">
                    <div class="file-icon">
                        <svg width="28" height="40" viewBox="0 0 28 40" version="1.1"
                             xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                            <defs>
                                <filter x="-50%" y="-50%" width="200%" height="200%" filterUnits="objectBoundingBox"
                                        id="filter">
                                    <feOffset dx="0" dy="2" in="SourceAlpha" result="shadowOffsetOuter"/>
                                    <feGaussianBlur stdDeviation="0" in="shadowOffsetOuter"
                                                    result="shadowBlurOuter"/>
                                    <feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.07 0"
                                                   in="shadowBlurOuter" type="matrix"
                                                   result="shadowMatrixOuter"/>
                                    <feMerge>
                                        <feMergeNode in="shadowMatrixOuter"/>
                                        <feMergeNode in="SourceGraphic"/>
                                    </feMerge>
                                </filter>
                            </defs>
                            <g stroke="none" stroke-width="2" fill="none" fill-rule="evenodd"
                               transform="translate(2, 2)">
                                <path d="M0,3.00741988 C0,1.34646775 1.34252415,0 2.99998588,0 L15.1166483,0 C17.0807354,0 24,6.91885725 24,8.87457593 L24,33.0035574 C24,34.6584469 22.6582294,36 21.0089096,36 L2.99109042,36 C1.33915679,36 0,34.6544607 0,32.9925801 L0,3.00741988 Z"
                                      stroke="#7289da" fill="#f4f6fc"/>
                                <path d="M17,1.09677336 C17,0.542040316 17.3147964,0.407097791 17.7133118,0.80556379 L23.1952031,6.28677654 C23.5891543,6.68067898 23.4552279,7 22.9039575,7 L18.0045574,7 C17.4497557,7 17,6.54676916 17,5.99556698 L17,1.09677336 Z"
                                      stroke="#7289da" fill="#f4f6fc" filter="url(#filter)"/>
                                <path d="M4,0 L5,0 L5,36 L4,36 L4,0 Z M0,3 L4,3 L4,4 L0,4 L0,3 Z M0,7 L4,7 L4,8 L0,8 L0,7 Z M0,11 L4,11 L4,12 L0,12 L0,11 Z M0,15 L4,15 L4,16 L0,16 L0,15 Z M0,19 L4,19 L4,20 L0,20 L0,19 Z M0,23 L4,23 L4,24 L0,24 L0,23 Z M0,31 L4,31 L4,32 L0,32 L0,31 Z M0,27 L4,27 L4,28 L0,28 L0,27 Z"
                                      fill="#7289da"/>
                                <path d="M23,9 L24,9 L24,36 L23,36 L23,9 Z M19,11 L23,11 L23,12 L19,12 L19,11 Z M19,15 L23,15 L23,16 L19,16 L19,15 Z M19,19 L23,19 L23,20 L19,20 L19,19 Z M19,23 L23,23 L23,24 L19,24 L19,23 Z M19,31 L23,31 L23,32 L19,32 L19,31 Z M19,27 L23,27 L23,28 L19,28 L19,27 Z"
                                      fill="#7289da"
                                      transform="translate(21.5, 22.5) scale(-1, 1) translate(-21.5, -22.5)"/>
                                <path d="M14.5039397,17.3759145 C15.1656928,17.7205743 15.165014,18.2797318 14.5039397,18.6240381 L10.1982101,20.8665842 C9.53645691,21.211244 9,20.8649547 9,20.0946469 L9,15.9053057 C9,15.1343167 9.53713571,14.7890621 10.1982101,15.1333684 L14.5039397,17.3759145 L14.5039397,17.3759145 Z"
                                      stroke="#7289da" fill="#f4f6fc"/>
                            </g>
                        </svg>
                    </div>
                    <div class="file-text">
                        <div class="file-name">{{file.name}}</div>
                        <div class="file-size">{{humanFileSize(file.size)}}</div>
                    </div>
                    <div class="file-download">
                        <svg width="24" height="24" viewBox="0 0 24 24">
                            <path d="M19,9h-4V3H9v6H5l7,7,7-7zM5,18v2h14v-2H5z"/>
                        </svg>
                    </div>
                </div>
                <div v-for="(embed, i) in json.embeds" v-bind:key="i">
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
                                <div class="description-content" v-if="embed.description">
                                    <markdown-highlight :text="embed.description"/>
                                </div>
                            </div>
                            <div class="fields" v-if="embed.fields">
                                <!-- TODO: Field inline -->
                                <div v-for="(field, i) in embed.fields" v-bind:key="i" class="field"
                                     style="grid-column: 1 / 13;">
                                    <div class="field-name">
                                        <div class="field-name-content">{{field.name}}</div>
                                    </div>
                                    <div class="field-value">
                                        <div class="field-value-content">
                                            <markdown-highlight :text="field.value"/>
                                        </div>
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
    </div>
</template>

<script>
    import MarkdownHighlight from "./MarkdownHighlight";

    export default {
        props: ['data'],
        components: {MarkdownHighlight},
        computed: {
            avatarUrl() {
                if (this.json.avatar_url) {
                    return this.json.avatar_url
                }
                return 'https://cdn.discordapp.com/embed/avatars/0.png'
            },
            messageTime() {
                return new Date().toLocaleTimeString().replace(/(.*)\D\d+/, '$1');
            },
            json() {
                return this.data.json
            },
            files() {
                return this.data.files
            }
        },
        methods: {
            humanFileSize(bytes, si = false, dp = 2) {
                if (!bytes) return

                const thresh = si ? 1000 : 1024;

                if (Math.abs(bytes) < thresh) {
                    return bytes + ' B';
                }

                const units = si
                    ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
                    : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
                let u = -1;
                const r = 10 ** dp;

                do {
                    bytes /= thresh;
                    ++u;
                } while (Math.round(Math.abs(bytes) * r) / r >= thresh && u < units.length - 1);


                return bytes.toFixed(dp) + ' ' + units[u];
            }
        }
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

            .file {
                width: 100%;
                max-width: 520px;
                padding: 10px;
                display: flex;
                -moz-box-align: center;
                align-items: center;
                border: 1px solid rgb(41, 43, 47);
                border-radius: 3px;
                background: rgb(47, 49, 54) none repeat scroll 0% 0%;
                overflow: hidden;

                .file-icon {
                    width: 30px;
                    height: 40px;
                    margin: 0px 8px 0px 0px;
                    display: flex;
                    -moz-box-align: center;
                    align-items: center;
                    -moz-box-pack: center;
                    justify-content: center;
                }

                .file-text {
                    flex: 1 1 0%;
                    white-space: nowrap;
                    text-overflow: ellipsis;
                    overflow: hidden;

                    .file-name {
                        max-width: 100%;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                        overflow-wrap: break-word;
                        display: block;
                        line-height: 1em;
                        color: rgb(0, 176, 244);
                        cursor: pointer;
                    }

                    .file-size {
                        color: rgb(114, 118, 125);
                        font-size: 12px;
                        line-height: 1.33333em;
                        font-weight: 300;
                    }
                }

                .file-download {
                    color: rgb(185, 187, 190);
                    cursor: pointer;

                    svg {
                        fill: currentcolor;
                    }
                }
            }
        }
    }
</style>