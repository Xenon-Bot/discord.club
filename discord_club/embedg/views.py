from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
import json
import requests
from django.shortcuts import reverse

from oauth.shortcuts import requires_ouath_user
from .models import Embed
from oauth import settings as oauth


@requires_ouath_user
def index(request):
    return render(request, 'embedg/index.html', {})


@requires_ouath_user
@require_http_methods(['POST', 'GET'])
def embeds(request):
    if request.method == 'POST':
        if request.POST.get('data') is None:
            return HttpResponseBadRequest()

        emb = Embed(user=request.user, data=str(request.POST['data']))
        emb.save()
        if Embed.objects.filter(user__id=request.user.id).count() >= 10:
            Embed.objects.earliest('timestamp').delete()

        return HttpResponse(status=200)

    else:
        embs = Embed.objects.filter(user__id=request.user.id)
        data = []
        for emb in embs:
            data.append({"id": emb.id, "timestamp": emb.timestamp_str})

        return HttpResponse(content=json.dumps(data), content_type='application/json')


@requires_ouath_user
@require_http_methods(['GET'])
def embed(request, embed_id):
    emb = get_object_or_404(Embed, id=embed_id)
    return HttpResponse(content=emb.data, content_type='application/json')


def webhook(request):
    code = request.GET.get('code', None)
    if code is None:
        return HttpResponseForbidden()

    data = {
        'client_id': oauth.CLIENT_ID,
        'client_secret': oauth.CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'scopes': 'webhook.incoming',
        'redirect_uri': request.build_absolute_uri(reverse('embedg:webhook')),
        'code': code
    }

    resp = requests.post('https://discordapp.com/api/oauth2/token', data=data, timeout=1)
    print(resp.status_code, resp.json())
    if resp.status_code != 200:
        return HttpResponseBadRequest()

    return render(request, 'embedg/create_webhook.html', {'webhook': json.dumps(resp.json()['webhook']['url'])})

