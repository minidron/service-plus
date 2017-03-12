from django.contrib import admin

from reversion.admin import VersionAdmin

from crm.models import Client

__all__ = (
    'ClientAdmin',
)


@admin.register(Client)
class ClientAdmin(VersionAdmin):
    pass
