from django import forms
from django.contrib import admin
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe

from dal import autocomplete

from crm.models import SparePart, SparePartCount

__all__ = (
    'SparePartAdmin',
)


class SparePartAdminForm(forms.ModelForm):
    count = forms.IntegerField(
        label='Кол-во', initial=1)

    class Meta:
        widgets = {
            'brand': autocomplete.ModelSelect2(url='brand-autocomplete'),
            'model': autocomplete.ModelSelect2(
                url='model-autocomplete', forward=['brand']),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        count = (self.instance.spare_part_counts.exclude(booking__isnull=False)
                                                .count())
        if count:
            self.fields['count'].initial = count


@admin.register(SparePartCount)
class SparePartCountAdmin(admin.ModelAdmin):
    """
    Удалить после создании виджета
    """
    pass


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    form = SparePartAdminForm

    list_display = (
        'title',
        'brand',
        'model',
        'purchase_price',
        'retail_price',
        'field_count',
    )

    def field_count(self, instance):
        return mark_safe(instance.spare_part_counts.count())
    field_count.short_description = 'Кол-во'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return (qs.select_related('brand', 'model')
                  .prefetch_related('spare_part_counts'))

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        post_save.send(sender=self.model, instance=obj, created=True,
                       count=form.cleaned_data['count'])
