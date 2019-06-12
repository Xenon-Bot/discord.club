from django.contrib import admin

from .models import Feedback, Link, Service, Supporter


class LinkInline(admin.TabularInline):
    extra = 1
    model = Link


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_front']
    inlines = [LinkInline]


admin.site.register(Service, ServiceAdmin)
admin.site.register(Feedback)
admin.site.register(Supporter)
