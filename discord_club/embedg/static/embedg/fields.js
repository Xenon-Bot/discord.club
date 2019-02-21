function triggerFormEvent(eventName, target) {
  var event = jQuery.Event(eventName);
  event.target = target;
  $('#form').trigger(event);
}

function addField(name, value, inline) {
  $('#fields').append(`
    <div class="form-row">
      <div class="form-group col">
        <input type="text" class="form-control embed-field field-name" placeholder="Name" value="${name || ''}">
      </div>
      <div class="form-group col">
        <textarea rows="1" class="form-control embed-field field-value" placeholder="Value">${value || ''}</textarea>
      </div>
      <div class="form-group col-auto">
        <div class="form-check">
          <input class="form-check-input embed-field field-inline" type="checkbox" ${inline ? 'checked' : ''}>
          <label class="form-check-label">Inline</label>
        </div>
      </div>
      <div class="col-auto ml-4">
        <button type="button" class="btn btn-danger" onclick="deleteField(this);"><i class="fas fa-minus"></i></button>
      </div>
    </div>
    `);
}

$(function() {
  $('#field-add').click(function() {
    addField();
    triggerFormEvent('input', $('<div class="embed-field"></div>'));
  });

  $('#fields-delete').click(function() {
    $('#fields').html('');
    triggerFormEvent('input', $('<div class="embed-field"></div>'));
  });
});

function deleteField(element) {
  $(element).parent().parent().remove();
  triggerFormEvent('input', $('<div class="embed-field"></div>'));
}
