from django.urls import reverse, NoReverseMatch

from .models import Service


def meta(request):
    return {
        "meta": {
            "name": "magicbots",
            "author": "Merlin Fuchs",
            "title": "Magic Bots",
            "description": "",
            "keywords": ""
        }
    }


def services(request):
    services = Service.objects.all()
    for service in services:
        if service.view:
            try:
                view_path = reverse(service.view)
            except NoReverseMatch:
                pass
            else:
                setattr(service, 'active', view_path == request.path)

    return {'services': services}