from django.contrib import admin

from .models import Redirect


class RedirectAdmin(admin.ModelAdmin):
    list_display = ['path', 'target', 'permanent']


admin.site.register(Redirect, RedirectAdmin)
