from django.urls import path

from .views import index, invite, api_invites, api_invite


app_name = 'invites'
urlpatterns = [
    path('', index, name='index'),
    path('api/', api_invites, name='api_invites'),
    path('api/<int:id>/', api_invite, name='api_invite'),
    path('<str:name>/', invite, name='invite'),
]
