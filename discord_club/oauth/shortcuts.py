from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlquote_plus

from .models import OauthUser
from . import settings


def redirect_to_discord(request, state='/'):
    return redirect(f'https://discordapp.com/api/oauth2/authorize?response_type=code&client_id={settings.CLIENT_ID}'
                    f'&scope={"%20".join(settings.SCOPES)}&state={urlquote_plus(state)}'
                    f'&redirect_uri={urlquote_plus(settings.REDIRECT_URI)}')


def requires_ouath_user(handler):
    def wrapper(request, *args, **kwargs):
        try:
            user = OauthUser.objects.get(id=str(request.session.get("user")))
        except:
            return redirect_to_discord(request, request.path)
        else:
            request.user = user
            return handler(request, *args, **kwargs)

    return wrapper
