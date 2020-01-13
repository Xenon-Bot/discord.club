from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect
from django.db.utils import IntegrityError
import json

from .models import Invite
from oauth.shortcuts import requires_ouath_user


def _validate_invite(name: str, code: str):
    if len(name.strip()) < 4 or len(name.strip()) > 50:
        return "Name must be between 4 and 50 in length."

    if len(code.strip()) < 3 or len(code.strip()) > 32:
        return "Code must be between 4 and 32 in length."

    return True


@requires_ouath_user
def index(request):
    return render(request, 'invites/index.html', {})


def invite(request, name):
    invite = get_object_or_404(Invite, name=name)
    return redirect('https://discord.gg/' + invite.code)


@require_http_methods(['POST', 'GET'])
@requires_ouath_user
def api_invites(request):
    if request.method == 'POST':
        data = request.POST
        valid = _validate_invite(data.get('name'), data.get('code'))
        if not isinstance(valid, str):
            invite = Invite(user=request.user, name=data.get('name'), code=data.get('code'))
            try:
                invite.save()
            except IntegrityError:
                return HttpResponse(status=400, content="A invite with that name already exists.")

        else:
            return HttpResponse(status=400, content=valid)

    else:
        invites = [{
            'id': invite.id,
            'name': invite.name,
            'code': invite.code
        } for invite in request.user.invite_set.all()]
        return HttpResponse(json.dumps(invites), content_type='application/json')

    return HttpResponse(status=200)


@require_http_methods(['PUT', 'DELETE'])
@requires_ouath_user
def api_invite(request, id):
    invite = get_object_or_404(Invite, id=id)
    if request.method == 'PUT':
        data = QueryDict(request.body)
        valid = _validate_invite(data.get('name'), data.get('code'))
        if not isinstance(valid, str):
            invite.name = data.get('name', invite.name)
            invite.code = data.get('code', invite.code)
            try:
                invite.save()
            except IntegrityError:
                return HttpResponse(status=400, content="A invite with that name already exists.")

        else:
            return HttpResponse(status=400, content=valid)

    else:
        invite.delete()

    return HttpResponse(status=200)
