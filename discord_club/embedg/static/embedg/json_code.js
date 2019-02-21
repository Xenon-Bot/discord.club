function VBColorToHEX(i) {
  var ret = "#000000";
  var rrggbb = i.toString(16);
  return ret.substring(0, 7 - rrggbb.length) + rrggbb;
}

function HEXToVBColor(rrggbb) {
  if (rrggbb.startsWith("#")) {
    rrggbb = rrggbb.substring(1);
  }
  return parseInt(rrggbb, 16);
}

$(function() {
  var json = {};

  function setPathInEmbed(path, value) {
    var schema = json;
    var pList = path.split('-');
    var len = pList.length;

    if (value == "" || value === undefined) {
      for (var y = len - 1; y >= 0; y--) {
        schema = json;
        for (var x = 0; x < y; x++) {
          schema = schema[pList[x]];
        }
        if (Object.keys(schema[pList[y]]).length == 0 || y == len - 1) {
          delete schema[pList[y]];
        }
      }
    } else {
      for (var i = 0; i < len - 1; i++) {
        var elem = pList[i];
        if (!schema[elem]) schema[elem] = {};
        schema = schema[elem];
      }

      schema[pList[len - 1]] = value;
    }
  }

  function updateForm(json, path) {
    path = path || '';
    if (path == '') {
      $('#fields').html('');
      $('#form').trigger("reset");
    }
    for (var key in json) {
      var value = json[key];
      if (path == '-embed-fields') {
        addField(value.name, value.value, value.inline);
      } else if (typeof value === 'object') {
        updateForm(value, path + '-' + key);
      } else {
        var id = (path + '-' + key).substring(1);
        value = id == 'embed-color' ? VBColorToHEX(value) : value;
        value = id == 'embed-timestamp' ? value.substring(0, value.length - 1) : value;
        $('#' + id).val(value);
      }
    }
  }

  $('#form').on('input', function(e) {
    var target = $(e.target);
    if (target.hasClass('embed-field')) {
      var fields = [];
      $('#fields').children().each(function() {
        var field = $(this);
        fields.push({
          'name': field.find('.field-name').val(),
          'value': field.find('.field-value').val(),
          'inline': field.find('.field-inline').prop('checked')
        });
      });
      setPathInEmbed('embed-fields', fields);
    } else {
      var value = target.attr('id') == 'embed-color' ? HEXToVBColor(target.val()) : target.val();
      setPathInEmbed(target.attr('id'), value);
    }
    $('#json').val(JSON.stringify(json, null, 4));

    updatePreview(json);
  });

  $('#json').on('input', function(e) {
    var target = $(e.target);
    try {
      var temp = JSON.parse(target.val());
      $('#parse-error').css('display', 'none');
      json = temp;
      updateForm(json);
    } catch (error) {
      $('#parse-error').css('display', 'block');
    }

    updatePreview(json);
  });

  $('#submit').click(function() {
    if ($('#webh-url').val() == '') {
      return;
    }
    var btn = $(this);
    btn.html('Sending Embed <span class="spinner-border spinner-border-sm text-dark ml-1" role="status"></span>');
    $.post(
      $('#webh-url').val(),
      JSON.stringify({
        'username': $('#webh-name').val(),
        'avatar_url': $('#webh-avatar-url').val(),
        'content': json.content,
        'embeds': [json.embed],
      }),
      null,
      'json'
    ).done(function(data) {
      $('#submit-alerts').html(`
          <div class="alert alert-success alert-dismissible fade show" role="alert">
            <h4 class="alert-heading">Successfully sent embed</h4>
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
        `);
    }).fail(function(data) {
      $('#submit-alerts').html(`
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
          <h4 class="alert-heading">${data.status} ${data.statusText}</h4>
          <p>Click <a target="_blank" href="https://leovoel.github.io/embed-visualizer/" class="alert-link">here</a> to check your json code</p>
          <hr>
          <textarea class="form-control" rows="5" readonly>${data.responseText}</textarea>
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        `);
    }).always(function(data) {
      btn.html('Send Embed');
    });
  });

  $('#json').val('{}');
  updateForm(json);
});
