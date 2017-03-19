from django.db.models import Count

from dal import autocomplete

from rest_framework import status, viewsets
from rest_framework.response import Response

from crm.filters import SparePartCountFilterSet, SparePartFilterSet
from crm.models import Brand, Job, Model, SparePart, SparePartCount
from crm.serializers import (
    JobSerializer,
    SparePartCountSerializer,
    SparePartSerializer,
)


class BrandAutocomplete(autocomplete.Select2QuerySetView):
    """
    Автокомплит бренда по его полному названию
    """
    def get_queryset(self):
        qs = Brand.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class ModelAutocomplete(autocomplete.Select2QuerySetView):
    """
    Автокомплит моделей устройств по их названию, а так же фильтр по бренду
    """
    def get_queryset(self):
        brand = self.forwarded.get('brand', None)
        qs = Model.objects.all()
        if not brand:
            qs = qs.none()
        else:
            qs = qs.filter(name__icontains=self.q, brand=brand)
        return qs


class JobViewSet(viewsets.ModelViewSet):
    """
    Список предоставляемых работ с ценой
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class SparePartCountViewSet(viewsets.ModelViewSet):
    """
    Запчасти
    """
    filter_class = SparePartCountFilterSet
    model = SparePartCount
    queryset = SparePartCount.objects.select_related('booking')
    serializer_class = SparePartCountSerializer

    def destroy(self, request, pk=None):
        obj = self.get_object()
        spare_part, created = SparePart.objects.get_or_create(
            title=obj.title, brand=obj.brand, model=obj.model,
            purchase_price=obj.purchase_price, retail_price=obj.retail_price)
        obj.booking = None
        obj.spare_part = spare_part
        obj.save()
        return Response({'status': 'SparePart update'},
                        status=status.HTTP_200_OK)

    def filter_queryset(self, queryset):
        if self.action == 'list':
            booking_filter = self.request.GET.get('booking')
            if not booking_filter:
                queryset = queryset.none()
        return super().filter_queryset(queryset)


class SparePartViewSet(viewsets.ModelViewSet):
    """
    Запчасти
    """
    filter_class = SparePartFilterSet
    model = SparePart
    queryset = (SparePart.objects.select_related('brand', 'model')
                                 .prefetch_related('spare_part_counts')
                                 .annotate(count=Count('spare_part_counts'))
                                 .filter(count__gte=1))
    serializer_class = SparePartSerializer

    def update(self, request, pk=None):
        obj = self.get_object()
        spare_part_count = obj.spare_part_counts.last()
        (SparePartCount.objects.filter(pk=spare_part_count.pk)
                               .update(booking_id=request.data['booking'],
                                       spare_part=None))
        return Response({'status': 'SparePartCount update'},
                        status=status.HTTP_200_OK)
