<template>
    <ul class="mt-3">
        <li v-for="(error, i) in errors" :key="i" v-html="error"/>
    </ul>
</template>
<script>
    function formatName(name) {
        return name.trim().replace("_", "-").replace(" ", "-")
    }

    export default {
        name: 'ResponseFormatter',
        props: ['response'],
        data() {
            return {
                errors: []
            }
        },
        methods: {
            computeErrors() {
                this.response.json().then(data => {
                    this.errors = []
                    const errors = data.errors
                    if (!errors) {
                        this.errors.push(data.message)
                        return
                    }

                    if (errors.embeds) {
                        if (errors.embeds._errors) {
                            for (let error of errors.embeds._errors) {
                                this.errors.push(`Embeds: ${error.message}`)
                            }
                        } else {
                            for (let pos in errors.embeds) {
                                let embed = errors.embeds[pos]

                                let level = embed
                                let name = ''
                                while (!level._errors) {
                                    const nextKey = Object.keys(level)[0]
                                    if (!nextKey) {
                                        break
                                    }
                                    name += ' ' + nextKey
                                    level = level[nextKey]
                                }

                                if (level._errors) {
                                    for (let error of level._errors) {
                                        this.errors.push(`Embed ${parseInt(pos) + 1}: <code>${formatName(name)}</code> is invalid (${error.message})`)
                                    }
                                }
                            }
                        }
                        delete errors.embeds
                    }

                    for (let key in errors) {
                        let name = key
                        let level = errors[key]
                        while (!level._errors) {
                            const nextKey = Object.keys(level)[0]
                            if (!nextKey) {
                                break
                            }
                            name += ' ' + nextKey
                            level = level[nextKey]
                        }

                        if (level._errors) {
                            for (let error of level._errors) {
                                this.errors.push(`<code>${formatName(name)}</code> is invalid (${error.message})`)
                            }
                        }
                    }
                })
            }
        },
        watch: {
            response() {
                if (!this.response) return
                if (!this.response.ok) {
                    this.computeErrors()
                }
            }
        }
    }
</script>