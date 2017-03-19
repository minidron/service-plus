import django_filters

from crm.models import SparePart, SparePartCount


class SparePartCountFilterSet(django_filters.FilterSet):
    class Meta:
        model = SparePartCount

        fields = (
            'booking',
        )


class SparePartFilterSet(django_filters.FilterSet):
    class Meta:
        model = SparePart

        fields = (
            'brand',
            'model',
        )
