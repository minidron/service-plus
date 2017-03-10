from django import template
from django.contrib.admin.templatetags.admin_list import result_list

from crm.utils import format_price


register = template.Library()

register.inclusion_tag(
    'crm/admin/booking_change_list_results.html')(result_list)


@register.simple_tag
def row_field(cl, field_name, index):
    field = getattr(cl.result_list[index], field_name)
    if hasattr(field, '__call__'):
        field = field()
    return field


@register.filter
def price(value):
    return format_price(value)
