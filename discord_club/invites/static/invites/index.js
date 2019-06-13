function showInvite(invite, edit) {
    $('#invites').append(`
        <div class="card my-3" id="${invite.id || ''}">
                <div class="card-body">
                    <div class="error"></div>
                    <div class="form-row pb-3">
                        <div class="col-12 col-md-6 py-1">
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <div class="input-group-text">discord.club/i/</div>
                                </div>
                                <input type="text" class="form-control form-control-lg invite-name" placeholder="Name" value="${invite.name || ''}"  ${edit ? '' : 'disabled'}>
                            </div>
                        </div>
                        <div class="col-12 col-md-6 py-1">
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <div class="input-group-text">discord.gg/</div>
                                </div>
                                <input type="text" class="form-control form-control-lg invite-code" placeholder="Invite Code" value="${invite.code || ''}" ${edit ? '' : 'disabled'}>
                            </div>
                        </div>
                    </div>
                    <button type="button" class="btn btn-danger" onclick="deleteInvite(this);"><i class="fas fa-trash-alt"></i></button>
                    <span class="invite-buttons">
                        ${edit ? '<button type="button" class="btn btn-success" onclick="saveInvite(this);"><i class="fas fa-save"></i></button>' : '<button type="button" class="btn btn-warning" onclick="editInvite(this);"><i class="fas fa-pen"></i></button>'}
                    </span>
                </div>
            </div>
    `);
}

function loadInvites() {
    $('#invites').html('');
    $.get('api/', function (invites) {
        invites.forEach(function (invite) {
            showInvite(invite, false);
        });
    });
}

function deleteInvite(obj) {
    var invite = $(obj).parent().parent();
    var id = invite.attr('id');
    if (id !== '') {
        $.ajax({
            url: 'api/' + id + '/',
            method: 'DELETE'
        }).always(function () {
            invite.remove();
            loadInvites();
        });
    } else {
        invite.remove();
        loadInvites();
    }
}

function editInvite(obj) {
    var invite = $(obj).parent().parent().parent();
    $('input', invite).attr('disabled', false);
    $('.invite-buttons', invite).html('<button type="button" class="btn btn-success" onclick="saveInvite(this);"><i class="fas fa-save"></i></button>');
}

function saveInvite(obj) {
    var invite = $(obj).parent().parent().parent();
    var id = invite.attr('id');
    var data = {
        name: $('.invite-name', invite).val(),
        code: $('.invite-code', invite).val()
    };

    if (data.name === '' || data.code === '') {
        return;
    }

    function done() {
        loadInvites();
        $('input', invite).attr('disabled', true);
        $('.invite-buttons', invite).html('<button type="button" class="btn btn-warning" onclick="editInvite(this);"><i class="fas fa-pen"></i></button>');
    }

    function saveFailed(response) {
         $('.error', invite).html(`
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <h4 class="alert-heading">${response.responseText}</h4>
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            `);
    }

    if (id !== '') {
        $.ajax({url: 'api/' + id + '/', data: data, method: 'PUT'}).fail(function () {
            return;
        }).fail(function (response) {
            saveFailed(response);
        }).done(function () {
            loadInvites();
        });

    } else {
        $.post('api/', data).fail(function () {
            return;
        }).fail(function (response) {
            saveFailed(response);
        }).done(function () {
            loadInvites();
        });
    }
}

$(function () {
    $.ajaxSetup({
        headers: {'X-CSRFToken': getCSRFToken()}
    });

    loadInvites();

    $('#add-invite').click(function () {
        showInvite({}, true);
    });
});