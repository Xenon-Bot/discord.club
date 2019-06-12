from django.shortcuts import render

from .models import Feedback, Supporter


def index(request):
    context = {
        'feedback': Feedback.objects.all(),
        'supporters': Supporter.objects.all()
    }
    return render(request, 'home/index.html', context)


def privacy(request):
    return render(request, 'home/privacy.html', {})


def cookies(request):
    return render(request, 'home/cookies.html', {})
