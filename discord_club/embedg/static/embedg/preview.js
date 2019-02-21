var markdown = window.markdownit({
  highlight: function(str, lang) {
    console.log("test");
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(lang, str).value;
      } catch (__) {}
    }

    return '';
  }
});


function updatePreview(json) {
  var prev = $('#preview');
  $('.user-name').html($('#webh-name').val() || 'Webhook');
  $('.avatar-large').css('background-image', `url(${$('#webh-avatar-url').val() || 'https://cdn.discordapp.com/embed/avatars/0.png'})`);

  $('.message-text', prev).html(markdown.render(json.content || ''));

  if ('embed' in json) {
    var embed = json.embed;
    $('.embed-color-pill', prev).css('background-color', $('#embed-color').val());
    prev.find('.embed-description').html(markdown.render(embed.description || ''));
    if (embed.author) {
      prev.find('._author').html(`
        <div class="embed-author">
          <img src="${embed.author.icon_url || ''}" role="presentation" class="embed-author-icon" alt="">
          <a target="_blank" rel="noreferrer" href="${embed.author.url || ''}" class="embed-author-name">${embed.author.name || ''}</a>
        </div>
      `);
    }
    if (embed.title) {
      prev.find('._title').html(`<a target="_blank" rel="noreferrer" href="${embed.url || ''}" class="embed-title">${markdown.renderInline(embed.title)}</a>`);
    }
    if (embed.thumbnail) {
      prev.find('.embed-rich-thumb').attr('src', embed.thumbnail.url || '');
    }
    if (embed.image) {
      prev.find('.embed-thumbnail-rich .image').attr('src', embed.image.url || '');
    }
    if (embed.footer) {
      prev.find('.embed-footer-icon').attr('src', embed.footer.icon_url || '');
      prev.find('.embed-footer-text').html(embed.footer.text || '');
    }
    if (embed.timestamp) {
      prev.find('.embed-footer-timestamp').html(' | ' + embed.timestamp);
    }
    var fieldWrapper = prev.find('.embed-fields');
    fieldWrapper.html('');
    if (embed.fields) {
      embed.fields.forEach(function(field) {
        fieldWrapper.append(`
          <div class="embed-field${field.inline ? 'embed-field-inline' : ''}">
            <div class="embed-field-name">${field.name}</div>
            <div class="embed-field-value markup">${markdown.renderInline(field.value)}</div>
          </div>
          `);
      });
    }
  }
}
