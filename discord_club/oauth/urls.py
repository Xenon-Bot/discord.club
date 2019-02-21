from django.urls import path

from .views import callback, login


app_name = 'oauth'
urlpatterns = [
    path('', login, name='login'),
    path('callback/', callback, name='callback')
]
