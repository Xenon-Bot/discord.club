var field_count = 0;
var form = document.forms["form"];

function VBColorToHEX(i) {
    var ret = "#000000";
    var rrggbb = i.toString(16);
    return ret.substring(0,7 - rrggbb.length) + rrggbb;
}

function HEXToVBColor(rrggbb) {
    if (rrggbb.startsWith("#")) {
        rrggbb = rrggbb.substring(1);
    }
    return parseInt(rrggbb, 16);
}

function updatePreviews() {
    document.getElementById('image_preview').src = form.elements['image'].value;
    document.getElementById('thumbnail_preview').src = form.elements['thumbnail'].value;
    document.getElementById('footer_icon_preview').src = form.elements['footer_icon'].value;
    document.getElementById('author_icon_preview').src = form.elements['author_icon'].value;
    document.getElementById('webhook_avatar_preview').src = form.elements['webhook_avatar'].value;
}

function evaluateWebhookUrl() {
    var element = form.elements["webhook_url"];
    var input = element.value;
    if (input.startsWith("https://discordapp.com/api/webhooks/")) {
        var segments = input.split("/");
        element.value = segments[segments.length-2] + "/" + segments[segments.length-1];
    }
}

function copyJson() {
    var json = document.forms["json_form"].elements["json"];
    json.select();
    document.execCommand("copy");
}

function addField() {
    if (field_count >= 20) {
        return
    }
    var count_string = field_count.toString();
    var fields = document.getElementById("fields");
    var new_field = document.createElement('div');
    new_field.innerHTML = `
        <div class="field" id="field_` + count_string + `">
            <div class="field-body">
                <div class="field">
                    <div class="control is-expanded">
                        <input required name="field_` + count_string + `_name" class="input" type="text" placeholder="Name">
                    </div>
                </div>
                <div class="field">
                    <div class="control is-expanded">
                        <textarea required rows="1" name="field_` + count_string + `_value" class="textarea" placeholder="Value"></textarea>
                    </div>
                </div>
                <div class="field">
                    <label class="checkbox">
                        <input name="field_` + count_string + `_inline" type="checkbox">
                        inline
                    </label>
                </div>
            </div>
        </div>
    `;
    fields.appendChild(new_field);
    field_count++;
}

function removeField() {
    var field = document.getElementById("field_" + (field_count - 1).toString());
    field.parentElement.removeChild(field);
    field_count--;
}

function removeFields() {
    for (i = 0; i < field_count; i++) {
        field = document.getElementById("field_" + i.toString());
        field.parentElement.removeChild(field);
    }
    field_count = 0;
}

function updateJson() {
    var fields = [];
    for (i = 0; i < field_count; i++) {
        fields.push({
            "name": form.elements["field_" + i.toString() + "_name"].value,
            "value": document.getElementsByName("field_" + i.toString() + "_value")[0].value,
            "inline": document.getElementsByName("field_" + i.toString() + "_inline")[0].checked,
        });
    }
    var json = {
        "content": form.elements["content"].value,
        "embed": {
            "title": form.elements["title"].value,
            "description": form.elements["description"].value,
            "url": form.elements["url"].value,
            "color": HEXToVBColor(form.elements["color"].value),
            "fields": fields,
            "thumbnail": {
                "url": form.elements["thumbnail"].value
            },
            "image": {
                "url": form.elements["image"].value
            },
            "author": {
                "name": form.elements["author_name"].value,
                "url": form.elements["author_url"].value,
                "icon_url": form.elements["author_icon"].value
            },
            "footer": {
                "text": form.elements["footer_text"].value,
                "icon_url": form.elements["footer_icon"].value
            }
        }
    };

    document.forms["json_form"].elements["json"].value = JSON.stringify(json);
}

function updateForm() {
    var object = JSON.parse(document.forms["json_form"].elements["json"].value);
    function getValue(...names) {
        var value = object;
        for (var i in names) {
            value = value[names[i]];
            if (value === undefined) {
                return "";
            }
        }
        return value;
    }

    form.elements["content"].value = getValue("content");
    form.elements["title"].value = getValue("embed", "title");
    form.elements["description"].value = getValue("embed", "description");
    form.elements["url"].value = getValue("embed", "url");
    form.elements["color"].value = VBColorToHEX(getValue("embed", "color"));
    form.elements["thumbnail"].value = getValue("embed", "thumbnail", "url");
    form.elements["image"].value = getValue("embed", "image", "url")
    form.elements["author_name"].value = getValue("embed", "author", "name");
    form.elements["author_url"].value = getValue("embed", "author", "url");
    form.elements["author_icon"].value = getValue("embed", "author", "icon_url");
    form.elements["footer_text"].value = getValue("embed", "footer", "text");
    form.elements["footer_icon"].value = getValue("embed", "footer", "icon_url");
    removeFields();
    for (var i in getValue("embed", "fields")) {
        addField();
        field = object.embed.fields[i];
        form.elements["field_" + i.toString() + "_name"].value = field.name;
        form.elements["field_" + i.toString() + "_value"].value = field.value;
        form.elements["field_" + i.toString() + "_inline"].checked = field.inline;
    }
}

document.addEventListener("DOMContentLoaded", function(event) {
    if (document.forms["json_form"].elements["json"].value == "") {
        updateJson();
    } else {
        updateForm();
    }
});