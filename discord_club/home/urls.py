from django.urls import path

from .views import handler404, handler500, index, privacy, cookies


handler404 = handler404
handler500 = handler500


app_name = 'home'
urlpatterns = [
    path('', index, name='index'),
    path('privacy/', privacy, name='privacy'),
    path('cookies/', cookies, name='cookies')
]
