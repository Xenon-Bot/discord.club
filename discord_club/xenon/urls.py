from django.urls import path

from .views import index


app_name = 'xenon'
urlpatterns = [
    path('', index, name='index')
]
