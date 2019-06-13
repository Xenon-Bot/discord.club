import requests
from django.shortcuts import reverse, redirect

from . import settings
from .shortcuts import redirect_to_discord
from .models import OauthUser


def login(request):
    return redirect_to_discord(request)


def callback(request):
    state = request.GET.get('state', '/')
    code = request.GET.get('code', None)
    if code is None:
        return login(request)

    data = {
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'scopes': ' '.join(settings.SCOPES),
        'redirect_uri': settings.REDIRECT_URI,
        'code': code
    }

    resp = requests.post('https://discordapp.com/api/oauth2/token', data=data, timeout=1)
    if resp.status_code != 200:
        return redirect_to_discord(request)

    tokens = resp.json()
    headers = {
        'Authorization': "Bearer " + tokens['access_token']
    }
    resp = requests.get('https://discordapp.com/api/users/@me', headers=headers, timeout=1)
    if resp.status_code != 200:
        return redirect_to_discord(request)

    user = resp.json()

    user_object = OauthUser(
        id=user['id'],
        name=user['username'],
        discriminator=user['discriminator'],
        email=user.get('email') or '',
        access_token=tokens['access_token'],
        refresh_token=tokens['refresh_token']
    )
    user_object.save()

    request.session['user'] = user['id']

    return redirect(state)
