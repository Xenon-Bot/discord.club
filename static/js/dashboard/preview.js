function makePreview() {
    const previewDom = $("#preview");
    previewDom.html("");
    previewDom.append(`
        <img src="${data.avatar_url ? data.avatar_url : "https://cdn.discordapp.com/embed/avatars/0.png"}" class="previewAvatar">
    `)

    let embedDom = "";
    if (data.embeds) {
        for (let embed of data.embeds) {
            let authorDom = "";
            if (embed.author) {
                let iconDom = ""
                if (embed.author.icon_url) {
                    iconDom = `<img src="${embed.author.icon_url}" alt="" class="previewEmbedAuthorIcon">`
                }
                authorDom = `
                    <div class="previewEmbedAuthor">
                        ${iconDom}
                        <a href="${embed.author.url ? embed.author.url : ""}" class="previewEmbedAuthorName">${embed.author.name}</a>
                    </div>
                `
            }

            let imageDom = ""
            if (embed.image) {
                imageDom = `<img src="${embed.image.url}" alt="" class="previewEmbedImage">`
            }

            let thumbnailDom = ""
            if (embed.thumbnail) {
                thumbnailDom = `<img src="${embed.thumbnail.url}" alt="" class="previewEmbedThumbnail">`
            }

            let footerDom = ""
            if (embed.footer) {
                if (embed.timestamp) {
                    footerDom = `
                    <div class="previewEmbedFooter">
                        <img src="${embed.footer.icon_url}" alt="" class="previewEmbedFooterIcon">
                        <span class="peviewEmbedFooterText">
                        ${embed.footer.text} • ${embed.timestamp}
                        </span>
                    </div>
                    `
                } else {
                    footerDom = `
                    <div class="previewEmbedFooter">
                        <img src="${embed.footer.icon_url}" alt="" class="previewEmbedFooterIcon">
                        <span class="peviewEmbedFooterText">
                        ${embed.footer.text}
                        </span>
                    </div>
                    `
                }
            } else if (embed.timestamp) {
                footerDom = `
                <div class="previewEmbedFooter">
                    <img src="${embed.footer.icon_url}" alt="" class="previewEmbedFooterIcon">
                    <span class="peviewEmbedFooterText">
                    ${embed.timestamp}
                    </span>
                </div>
                `
            }

            fieldsDom = ""
            if (embed.fields) {
                for (let field of embed.fields) {
                    fieldsDom += `
                    <div class="previewEmbedField">
                        <div class="previewEmbedFieldName">
                            ${field.name}
                        </div>
                        <div class="previewEmbedFieldValue">
                            ${field.value}
                        </div>
                    </div>
                    `
                }
            }

            embedDom += `
                <div class="previewEmbed" style="border-left-color: #${embed.color.toString(16)}">
                    <div class="previewEmbedContent">
                        ${authorDom}
                        <div class="previewEmbedTitle">
                            ${embed.title ? embed.title : ""}
                        </div>
                        <div class="previewEmbedDescription">
                            ${embed.description ? embed.description : ""}
                        </div>
                        <div class="previewEmbedFields">
                            ${fieldsDom}
                        </div>
                        ${imageDom}
                        ${thumbnailDom}
                        ${footerDom}
                    </div>
                </div>
                <br/>
            `
        }
    }

    previewDom.append(`
        <div class="previewBody">
            <div class="previewName">
                ${data.username ? data.username : "Captain Hook"}
                <span class="previewBotTag">BOT</span>
            </div>
            <div class="previewContent">
                ${data.content ? data.content : ""}
            </div>
            <div class="previewAttachments">
            </div>
            <div class="previewEmbeds">
                ${embedDom}
            </div>
        </div>
    `)

    // files are loaded async (last)
    const attachmentDom = $(".previewAttachments");
    const attachments = $("#attachments").find("input");
    for (let attach of attachments) {
        attach = $(attach);
        const fileName = attach.val();
        const files = attach.prop("files")
        if (fileName && files.length > 0) {
            const fr = new FileReader();
            fr.onload = function() {
                attachmentDom.append(`
                <img src="${fr.result}" alt="${fileName}" class="previewAttachment">
                `)
            }
            fr.readAsDataURL(files[0]);
        }
    }
}