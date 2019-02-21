from django.urls import path

from .views import index, privacy, cookies


app_name = 'home'
urlpatterns = [
    path('', index, name='index'),
    path('privacy/', privacy, name='privacy'),
    path('cookies/', cookies, name='cookies')
]
