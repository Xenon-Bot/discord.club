function getCSRFToken() {
    return $('input[name=csrfmiddlewaretoken]').val();
}