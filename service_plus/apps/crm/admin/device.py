from django.contrib import admin

from crm.models import Brand, Model

__all__ = (
    'BrandAdmin',
    'ModelAdmin',
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    pass
