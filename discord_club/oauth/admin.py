from django.contrib import admin

from .models import OauthUser


def discord_tag(model):
    return model.name + "#" + model.discriminator


class OauthUserAdmin(admin.ModelAdmin):
    list_display = [discord_tag, 'id', 'email']


admin.site.register(OauthUser, OauthUserAdmin)
