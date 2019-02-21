from django.shortcuts import get_object_or_404, redirect

from .models import Redirect


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            red = get_object_or_404(Redirect, path=request.path.strip('/'))
            return redirect(red.target, permanent=red.permanent or False)

        return response
