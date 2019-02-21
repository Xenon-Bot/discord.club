from django.contrib import admin

from .models import OauthUser


class OauthUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'discriminator', 'email']


admin.site.register(OauthUser, OauthUserAdmin)
