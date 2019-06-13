from django.contrib import admin

from .models import Invite


class InviteAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'code']


admin.site.register(Invite)

