from django import forms
from django.contrib import admin

from dal import autocomplete

from crm.models import Brand, Model, ReplacementDevice

__all__ = (
    'BrandAdmin',
    'ModelAdmin',
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


class ModelAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'brand': autocomplete.ModelSelect2(url='brand-autocomplete'),
        }


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    form = ModelAdminForm


class ReplacementDeviceAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'brand': autocomplete.ModelSelect2(url='brand-autocomplete'),
            'model': autocomplete.ModelSelect2(url='model-autocomplete',
                                               forward=['brand']),
        }


@admin.register(ReplacementDevice)
class ReplacementDeviceAdmin(admin.ModelAdmin):
    form = ReplacementDeviceAdminForm
