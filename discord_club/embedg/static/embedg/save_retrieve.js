function loadAvailableEmbeds() {
    var avEmbeds = $('#available-embeds');
    $.getJSON('embeds/', function (embeds) {
        avEmbeds.html('');
        for (var embed of embeds) {
            avEmbeds.append(`<a class="dropdown-item" onclick="loadEmbed(${embed.id})">${embed.timestamp}</a>`);
        }
    });
}

function loadEmbed(id) {
    $.getJSON(`embeds/${id}/`, function (data) {
        var json = $('#json');
        json.val(JSON.stringify(data, null, 4));
        json.trigger('input');
    });
}

$(function () {
    loadAvailableEmbeds();

    $('#save-embed').click(function () {
        var data = {
            data: $('#json').val(),
            csrfmiddlewaretoken: getCSRFToken()
        };
        $.post('embeds/', data);
        loadAvailableEmbeds();
    });
});