$(function () {
    var opened;
    $('#create-webhook').click(function () {
        opened = window.open(
            'https://discordapp.com/api/oauth2/authorize?client_id=465946982339444746&redirect_uri=http%3A%2F%2Fbeta.discord.club%2Fembedg%2Fwebhook%2F&response_type=code&scope=webhook.incoming',
            '_blank',
            'height=720,width=1080'
        );
    });

    $(window).on('message onmessage', function (e) {
        var original = e.originalEvent;
        console.log(original.source);
        if (original.source === opened) {
            $('#webh-url').val(original.data);
        }
    });
});