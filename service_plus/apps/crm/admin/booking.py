from django import forms
from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import formats
from django.utils.safestring import mark_safe

from dal import autocomplete

from reversion.admin import VersionAdmin

from crm.forms import BookingForm
from crm.models import Booking
from crm.utils import format_price

__all__ = (
    'BookingAdmin',
)


class BookingAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'brand': autocomplete.ModelSelect2(url='brand-autocomplete'),
            'model': autocomplete.ModelSelect2(
                url='model-autocomplete', forward=['brand']),
        }


class StateFilter(admin.ChoicesFieldListFilter):
    template = 'crm/admin/state_filter.html'


@admin.register(Booking)
class BookingAdmin(VersionAdmin):
    actions = None
    change_list_template = 'crm/admin/booking_change_list.html'
    form = BookingAdminForm

    list_display = (
        'field_id',
        'field_model',
        'imei',
        'field_estimated_cost',
        'field_estimated_date',
        'client_name',
        'field_created',
        'field_ready_date',
        'field_close_date',
        'field_open',
    )

    list_filter = (
        ('state', StateFilter),
    )

    fieldsets = (
        (None, {
            'fields': (
                'state',
            ),
        }),
        ('Предварительные данные клиента', {
            'fields': (
                'client',
                'client_name',
                'client_characteristic',
                'client_phone',
                'client_email',
                'client_address',
            ),
        }),
        ('Устройство', {
            'fields': (
                'imei',
                'brand',
                'model',
            ),
        }),
        ('Комплектация', {
            'fields': (
                ('has_device', 'has_battery', 'has_charger'),
                ('has_memory_card', 'has_sim', 'has_bag_cover'),
                'additional_kit',
            ),
        }),
        ('Неисправность', {
            'fields': (
                'problem',
                'note',
            ),
        }),
        (None, {
            'fields': (
                ('estimated_date', 'is_urgently'),
                'estimated_cost',
            ),
        }),
    )

    readonly_fields = (
        'state',
    )

    manager_fieldsets = (
        (None, {
            'fields': (
                'state',
            ),
        }),
    )

    class Media:
        css = {
            'all': (
                'crm/admin/css/style.css',
            )
        }

    def field_id(self, instance):
        return mark_safe('№ %s' % instance.id)
    field_id.admin_order_field = 'id'
    field_id.short_description = 'Номер'

    def field_estimated_date(self, instance):
        if instance.estimated_date:
            return mark_safe(
                formats.date_format(instance.estimated_date, 'j E'))
    field_estimated_date.admin_order_field = 'estimated_date'
    field_estimated_date.short_description = 'Пред. срок'

    def field_estimated_cost(self, instance):
        if instance.estimated_cost:
            return mark_safe(format_price(instance.estimated_cost))
    field_estimated_cost.admin_order_field = 'estimated_cost'
    field_estimated_cost.short_description = 'Пред. цена'

    def field_model(self, instance):
        return mark_safe(' '.join(
            filter(None, [getattr(instance.brand, 'name', None),
                          getattr(instance.model, 'name', None)])))
    field_model.admin_order_field = 'field_model'
    field_model.short_description = 'Модель'

    def field_created(self, instance):
        return mark_safe(instance.created.strftime('%d.%m.%Y - %-H:%M'))
    field_created.admin_order_field = 'created'
    field_created.short_description = 'Принят'

    def field_ready_date(self, instance):
        if instance.ready_date:
            return mark_safe(instance.ready_date.strftime('%d.%m.%Y - %-H:%M'))
    field_ready_date.admin_order_field = 'ready_date'
    field_ready_date.short_description = 'Готов'

    def field_close_date(self, instance):
        if instance.close_date:
            return mark_safe(instance.close_date.strftime('%d.%m.%Y - %-H:%M'))
    field_close_date.admin_order_field = 'close_date'
    field_close_date.short_description = 'Выдан'

    def field_open(self, instance):
        info = self.model._meta.app_label, self.model._meta.model_name
        action_open = '<a href="%s">открыть</a>' % reverse(
            'admin:%s_%s_review' % info, args=[instance.pk])
        return mark_safe('%s' % action_open)
    field_open.short_description = ''

    def get_fieldsets(self, request, obj=None):
        """
        Возвращаем список полей, в зависимости от прав пользователя
        """
        return super().get_fieldsets(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('brand', 'model')

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = [
            url(r'^(\d+)/review/$',
                self.admin_site.admin_view(self.review_view),
                name='%s_%s_review' % info),
        ]
        urls.extend(super().get_urls())
        return urls

    def review_view(self, request, object_id):
        booking = get_object_or_404(self.get_queryset(request), pk=object_id)
        form = BookingForm(request.POST or None, instance=booking)
        info = self.model._meta.app_label, self.model._meta.model_name
        if request.POST:
            save = request.POST.get('save')
            transition = request.POST.get('transition')
            if form.is_valid():
                if save == '_continue':
                    form.save()
                    return redirect('admin:%s_%s_review' % info, object_id)
                elif transition:
                    getattr(form.instance, transition)()
                    form.instance.save()
                    return redirect('admin:%s_%s_review' % info, object_id)
        title = (
            '<span class="booking-status %s" title="%s">Заявка № %s</span>' % (
                booking.state, booking.get_state_display(), booking.pk))
        context = {
            'form': form,
            'media': self.media,
            'object': booking,
            'opts': self.opts,
            'title': mark_safe(title),
        }
        return render(request, 'crm/admin/booking_review.html', context)
