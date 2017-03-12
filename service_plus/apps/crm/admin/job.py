from django.contrib import admin

from crm.models import Job

__all__ = (
    'JobAdmin',
)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
    )
