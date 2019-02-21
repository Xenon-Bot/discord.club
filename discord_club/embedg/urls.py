from django.urls import path

from .views import index, embed, embeds, webhook


app_name = 'embedg'
urlpatterns = [
    path('', index, name='index'),
    path('embeds/', embeds, name='embeds'),
    path('embeds/<int:embed_id>/', embed, name='embed'),
    path('webhook/', webhook, name='webhook')
]
