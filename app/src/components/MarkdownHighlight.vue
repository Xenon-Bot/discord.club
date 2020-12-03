<template>
    <div v-html="highlightedText"></div>
</template>
<script>
    export default {
        name: 'MarkdownHighlight',
        props: ['text'],
        computed: {
            highlightedText() {
                if (!this.text) return null

                return this.text
                    .replace(/&/g, "&amp;")
                    .replace(/</g, "&lt;")
                    .replace(/>/g, "&gt;")
                    .replace(/"/g, "&quot;")
                    .replace(/'/g, "&#039;")

                    .replace(/\*\*([\s\S]*?)\*\*/g, `<b class="highlight-bold">$1</b>`)
                    .replace(/\*([\s\S]*?)\*/g, `<i class="highlight-italic">$1</i>`)
                    .replace(/__([\s\S]*?)__/g, `<u class="highlight-underline">$1</u>`)
                    .replace(/~~([\s\S]*?)~~/g, `<span class="highlight-strike">$1</span>`)
                    .replace(/```(\S+\n|\n)?([\s\S]*?)\n?```/g, `<span class="highlight-code">$2</span>`)
                    .replace(/`([\s\S]*?)`/g, `<span class="highlight-monospace">$1</span>`)
                    .replace(/\[([\w\s\d]+)\]\((https?:\/\/[\w\d./?=#]+)\)/g, `<a class="highlight-link" href="$2" target="_blank">$1</a>`)
                    .replace(/(\s)(&lt;)?(https?:\/\/[\w\d./?=#]+)(&gt;)?(\s)/g, `<a class="highlight-link" href="$3" target="_blank">$1$3$5</a>`)
                    .replace(/&lt;(:\w+:)([0-9]+)&gt;/g, `<img  src="https://cdn.discordapp.com/emojis/$2.png" alt="$1" class="highlight-emoji"/>`)
                    .replace(/&lt;(a:\w+:)([0-9]+)&gt;/g, `<img  src="https://cdn.discordapp.com/emojis/$2.gif" alt="$1" class="highlight-emoji"/>`)
                    .replace(/(&lt;(?:@|@!|@&amp;|#)[0-9]+&gt;)/g, `<span class="highlight-mention">$1</span>`)
                    .replace(/(@everyone|@here)/g, `<span class="highlight-mention">$1</span>`)
            },
        }
    }
</script>
<style lang="scss">
    .highlight-emoji {
        width: 1.375em;
        height: 1.375em;
    }

    .highlight-bold {
        color: white;
        font-weight: bold;
    }

    .highlight-italic {
        font-style: italic;
    }

    .highlight-underline {
        text-decoration: underline;
    }

    .highlight-strike {
        text-decoration: line-through;
    }

    .highlight-code {
        display: block;
        background-color: rgb(47, 49, 54);
        border: 1px solid rgb(32, 34, 37);
        padding: 0.5em;
        max-width: 90%;
        margin: 6px 0 0;
        border-radius: 4px;
        white-space: pre-wrap;
        line-height: 1.125rem;
        color: rgb(185, 187, 190);
        font-size: 0.875rem;
    }

    .highlight-monospace {
        padding: 0.2em;
        margin: -0.2em 0px;
        border-radius: 3px;
        background: rgb(47, 49, 54) none repeat scroll 0% 0%;
        font-size: 0.85em;
        line-height: 1.125rem;
        white-space: pre-wrap;
    }

    .highlight-code, .highlight-monospace {
        font-family: Consolas, Andale Mono WT, Andale Mono, Lucida Console, Lucida Sans Typewriter, DejaVu Sans Mono, Bitstream Vera Sans Mono, Liberation Mono, Nimbus Mono L, Monaco, Courier New, Courier, monospace;
    }

    .highlight-link {
        color: #00b0f4;

        &:hover {
            color: #00b0f4;
        }
    }

    .highlight-mention {
        background-color: rgba(114, 137, 218, .1);
        color: #7289da
    }
</style>