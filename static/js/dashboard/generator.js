const msgAttributes = {
    "username": "#webhookName",
    "avatar_url": "#webhookAvatar",
    "content": "#content"
};
const embedAttributes = {
    "title": ".embedTitle",
    "description": ".embedDescription",
    "timestamp": ".embedTimestamp",
    "author.name": ".embedAuthorName",
    "author.url": ".embedAuthorUrl",
    "author.icon_url": ".embedAuthorIcon",
    "thumbnail.url": ".embedThumbnailUrl",
    "image.url": ".embedImageUrl",
    "footer.text": ".embedFooterText",
    "footer.icon_url": ".embedFooterIcon"
};
const embedFieldAttributes = {
    "name": ".embedFieldName",
    "value": ".embedFieldValue"
};

let data = {};

function setPathInObject(object, path, value) {
    let schema = object;
    let pList = path.split('.');
    let len = pList.length;

    if (!value) {
        for (let y = len - 1; y >= 0; y--) {
            schema = object;
            for (let x = 0; x < y; x++) {
                schema = schema[pList[x]];
            }

            if (!schema) {
                continue;
            }

            if (!schema[pList[y]] || Object.keys(schema[pList[y]]).length == 0 || y == len - 1) {
                delete schema[pList[y]];
            }
        }
    } else {
        for (let i = 0; i < len - 1; i++) {
            let elem = pList[i];
            if (!schema[elem]) schema[elem] = {};
            schema = schema[elem];
        }

        schema[pList[len - 1]] = value;
    }
}

function getPathInObject(object, path) {
    let schema = object;
    let pList = path.split('.');
    for (let p of pList) {
        if (!schema) return null;
        schema = schema[p];
    }

    return schema;
}

function updateJSON() {
    data = {
        embeds: []
    };

    for (let msgPath in msgAttributes) {
        let msgValue = $(msgAttributes[msgPath]).val();
        setPathInObject(data, msgPath, msgValue);
    }

    const embedDoms = $("#embeds").find(".embed");
    for (let embedDom of embedDoms) {
        embedDom = $(embedDom);

        const embed = {};
        for (let embedPath in embedAttributes) {
            let embedValue = embedDom.find(embedAttributes[embedPath]).val();
            setPathInObject(embed, embedPath, embedValue);
        }
        embed.color = parseInt("0x" + embedDom.find(".embedColor").val().substring(1));

        const fields = [];
        for (let embedFieldDom of embedDom.find(".embedField")) {
            embedFieldDom = $(embedFieldDom);

            const field = {};
            for (let fieldPath in embedFieldAttributes) {
                let fieldValue = embedFieldDom.find(embedFieldAttributes[fieldPath]).val();
                setPathInObject(field, fieldPath, fieldValue);
            }

            setPathInObject(field, "inline", embedFieldDom.find(".embedFieldInline").prop("checked"));

            if (Object.keys(field).length > 0) {
                fields.push(field);
            }
        }
        if (fields.length > 0) {
            embed.fields = fields;
        }

        if (Object.keys(embed).length > 0) {
            data.embeds.push(embed);
        }
    }

    $("#json").val(JSON.stringify(data, null, 4));
    window.localStorage.setItem("lastEmbed", JSON.stringify(data));
}

function updateForm() {
    const dataClone = JSON.parse(JSON.stringify(data));
    for (let msgPath in msgAttributes) {
        $(msgAttributes[msgPath]).val(getPathInObject(dataClone, msgPath));
    }

    deleteEmbeds();
    if (dataClone.embeds) {
        let embedIndex = 0;
        for (let embed of dataClone.embeds) {
            const embedDom = addEmbed(embedIndex === 0);
            for (let embedPath in embedAttributes) {
                embedDom.find(embedAttributes[embedPath]).val(getPathInObject(embed, embedPath));
                if (embed.color !== null || embed.color !== undefined) {
                    embedDom.find(".embedColor").val("#" + embed.color.toString(16))
                }
            }

            if (embed.fields) {
                for (let field of embed.fields) {
                    const fieldDom = addField(embedDom);
                    for (let fieldPath in embedFieldAttributes) {
                        fieldDom.find(embedFieldAttributes[fieldPath]).val(getPathInObject(field, fieldPath));
                    }
                    if (field.inline) {
                        fieldDom.find(".embedFieldInline").prop("checked", true);
                    }
                }
            }

            embedIndex++;
        }
    }

    // json might have changed due to inconsistencies
    updateJSON();
}

function addAttachment() {
    $("#attachments").append(`
                <div class="form-row attachment">
                    <div class="form-group col">
                        <input type="file" class="form-control-file">
                    </div>
                    <div class="col-auto">
                        <button type="button" class="btn btn-sm btn-outline-danger" onclick="deleteAttachment(this)">
                            <i class="material-icons float-left text-danger">remove_circle</i>
                        </button>
                    </div>
                </div>
            `);
}

function deleteAttachments() {
    $("#attachments").empty();
}

function deleteAttachment(it) {
    $(it).closest(".attachment").remove();
}

function addEmbed(show) {
    const embedDom = $("#embeds");
    if (embedDom.children().length >= 10) {
        showAlert("You can't add more than 10 embeds", "danger");
        return;
    }

    embedDom.append(`
                <div class="embed card my-3">
                    <div class="card-body">
                        <div class="form-row">
                            <div class="form-group col-10">
                                <input type="text" class="form-control embedTitle" placeholder="Title" maxlength="256">
                            </div>
                            <div class="form-group col-2">
                                <input type="color" class="form-control embedColor" value="#1f2225">
                            </div>
                        </div>
                        <div class="collapse${show ? ' show' : ''}">
                            <div class="form-group">
                                <textarea rows="5" class="form-control embedDescription" placeholder="Description" spellcheck="false" maxlength="2048"></textarea>
                            </div>
                            <div class="form-group pb-3">
                                <input type="url" class="form-control embedUrl" placeholder="Url">
                            </div>

                            <label>Author</label>
                            <div class="form-row">
                                <div class="form-group col">
                                    <input type="text" class="form-control embedAuthorName" placeholder="Name" maxlength="256">
                                </div>
                                <div class="form-group col">
                                    <input type="url" class="form-control embedAuthorIcon" placeholder="Icon-Url">
                                </div>
                            </div>
                            <div class="form-group pb-3">
                                <input type="text" class="form-control embedAuthorUrl" placeholder="Url">
                            </div>

                            <label>Images</label>
                            <div class="form-group">
                                <input type="url" class="form-control embedThumbnailUrl" placeholder="Thumbnail-Url">
                            </div>
                            <div class="form-group pb-3">
                                <input type="url" class="form-control embedImageUrl" placeholder="Image-Url">
                            </div>

                            <label>Footer</label>
                            <div class="form-row">
                                <div class="form-group col">
                                    <input type="text" class="form-control embedFooterText" placeholder="Text" maxlength="2048">
                                </div>
                                <div class="form-group col">
                                    <input type="datetime-local" class="form-control embedTimestamp" step="0.001">
                                </div>
                            </div>
                            <div class="form-group pb-3">
                                <input type="url" class="form-control embedFooterIcon" placeholder="Icon-Url">
                            </div>

                            <label>Fields</label>
                            <div class="embedFields"></div>
                            <button class="btn btn-sm btn-outline-success" onclick="addField(this)" type="button">
                                <i class="material-icons float-left text-success">add_circle</i>
                            </button>
                            <button class="btn btn-sm btn-outline-danger" onclick="deleteFields(this)" type="button">
                                <i class="material-icons float-left text-danger">delete</i>
                            </button>
                        </div>

                        <div class="float-right">
                            <button class="btn btn-sm btn-outline-danger" onclick="deleteEmbed(this)" type="button">
                                <i id="embedAdd" class="material-icons float-left text-danger">remove_circle</i>
                            </button>
                            <button class="btn btn-sm btn-outline-primary embedCollapse" onclick="collapseEmbed(this)" type="button">
                                <i id="embedAdd" class="material-icons float-left text-primary">${show ? 'expand_less' : 'expand_more'}</i>
                            </button>
                        </div>
                    </div>
                </div>
            `);

    updateJSON();
    return embedDom.find(".embed").last();
}

function collapseEmbed(it) {
    const embedDom = $(it).closest(".embed");
    const collapse = embedDom.find(".collapse");
    const collapseButton = embedDom.find(".embedCollapse i");

    if (collapse.hasClass("show")) {
        collapseButton.html("expand_more");
    } else {
        collapseButton.html("expand_less");
    }
    collapse.collapse("toggle");
}

function deleteEmbed(it) {
    $(it).closest(".embed").remove();
    updateJSON();
}

function deleteEmbeds() {
    $("#embeds").empty();
    updateJSON();
}

function addField(it) {
    const embedDom = $(it).closest(".embed");
    const fieldDom = embedDom.find(".embedFields");
    if (fieldDom.children().length >= 25) {
        showAlert("You can't add more than 10 fields per embed", "danger");
        return;
    }

    fieldDom.append(`
                <div class="form-row embedField">
                    <div class="form-group col">
                        <input type="text" class="form-control embedFieldName" placeholder="Name" maxlength="256">
                    </div>
                    <div class="form-group col">
                        <textarea rows="1" class="form-control embedFieldValue" placeholder="Value" maxlength="1024"></textarea>
                    </div>
                    <div class="form-group col-auto">
                        <div class="form-check">
                            <input class="form-check-input embedFieldInline" type="checkbox">
                            <label class="form-check-label">Inline</label>
                        </div>
                    </div>
                    <div class="col-auto ml-4">
                        <button type="button" class="btn btn-sm btn-outline-danger" onclick="deleteField(this)">
                            <i id="embedAdd" class="material-icons float-left text-danger">remove_circle</i>
                        </button>
                    </div>
                </div>
            `);

    updateJSON();
    return fieldDom.find(".embedField").last();
}

function deleteField(it) {
    $(it).closest(".embedField").remove();
    updateJSON();
}

function deleteFields(it) {
    const embedDom = $(it).closest(".embed");
    embedDom.find(".embedFields").empty();
    updateJSON();
}

function validateMessage() {
    const urlExpression = new RegExp(/https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/gi);

    if (data.content && content.length > 2000) {
        console.log("content > 2000")
        return false;
    }

    if (data.avatar_url && !data.avatar_url.match(urlExpression)) {
        console.log("invalid avatar url")
        return false;
    }

    if (data.embeds) {
        let embedNumber = 1;
        for (let embed of data.embeds) {
            let totalLength = 0;

            function validateLength(value, name, maxLength) {
                if (value == undefined || value == null) return true;

                totalLength += value.length;
                if (value.length > maxLength) {
                    alert("embbed " + embedNumber + " - " + name + " > " + maxLength);
                    return false;
                }
                return true;
            }

            function validateUrl(value, name) {
                if (value && !value.match(urlExpression)) {
                    alert("embbed " + embedNumber + " - " + name + " is an invalid url")
                    return false;
                }
                return true;
            }

            if (!validateLength(embed.title, "title", 256)) return false;
            if (!validateLength(embed.description, "description", 2048)) return false;
            if (embed.author) {
                if (!validateLength(embed.author.name, "author name", 256)) return false;
                if (!validateUrl(embed.author.icon_url, "author icon url")) return false;
                if (!validateUrl(embed.author.url, "author url")) return false;
            }

            if (embed.image) {
                if (!validateUrl(embed.image.url, "image url")) return false;
            }

            if (embed.thumbnail) {
                if (!validateUrl(embed.thumbnail.url, "thumbnail url")) return false;
            }

            if (embed.fields) {
                let fieldNumber = 1;
                for (let field of embed.fields) {
                    if (!validateLength(field.name, "field " + fieldNumber, 256)) return false;
                    if (!validateLength(field.value, "field " + fieldNumber, 1024)) return false;
                    fieldNumber++;
                }
            }

            if (embed.footer) {
                if (!validateLength(embed.footer.text, "footer text", 2048)) return false;
                if (!validateUrl(embed.footer.icon_url, "footer icon url")) return false;
            }

            if (totalLength > 6000) {
                alert("embbed " + embedNumber + " - " + "total length > 6000");
                return false;
            }

            embedNumber++;
        }
    }

    return true;
}

function sendMessage() {
    if (!validateMessage()) return;

    const payload = new FormData();
    payload.append("payload_json", JSON.stringify(data));
    const attachmentDoms = $("#attachments").find("input");
    let fileNumber = 0;
    for (let attachmentDom of attachmentDoms) {
        attachmentDom = $(attachmentDom);
        const fileName = attachmentDom.val();
        if (fileName) {
            payload.append("file" + fileNumber, attachmentDom.prop("files")[0], fileName);
            fileNumber++;
        }
    }

    $.post({
        url: $("#webhookUrl").val(),
        data: payload,
        processData: false,
        contentType: false
    }).always(r => {
        console.log(r)
    })
}

$(() => {
    $("#form").change(updateJSON);
    $("#json").change(() => {
        data = JSON.parse($("#json").val())
        updateForm();
    });

    const lastEmbed = window.localStorage.getItem("lastEmbed");
    if (lastEmbed) {
        data = JSON.parse(lastEmbed);
        updateForm();
    } else {
        addEmbed(true);
    }
})