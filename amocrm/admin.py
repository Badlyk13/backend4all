from django.contrib import admin

from amocrm.models import Client


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'amo_url', 'get_acctoken', 'get_reftoken', 'client_id', 'client_secret', 'is_active', 'registered_at')

    def get_acctoken(self, obj):
        if obj.access_token:
            return 'Ok'
        return 'Not used'

    def get_reftoken(self, obj):
        if obj.refresh_token:
            return 'Ok'
        return 'Not used'