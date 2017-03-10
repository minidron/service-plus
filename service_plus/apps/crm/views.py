from dal import autocomplete

from crm.models import Brand, Model


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
        elif self.q:
            qs = qs.filter(name__icontains=self.q, brand__name=brand)
        return qs
