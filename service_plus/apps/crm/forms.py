from django import forms
from django.db.models import Q

from crm.models import Booking, State


class BaseBookingForm(forms.ModelForm):
    """
    Базовый класс формы заявки
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.change_field_attribute(
            'master', 'label_from_instance', self.master_label)
        self.change_field_attribute(
            'replacement_device', 'queryset',
            self.available_replacement_device())

    @staticmethod
    def master_label(obj):
        """
        Показываем фамилию и имя вместо логина
        """
        name = ' '.join(filter(None, [obj.last_name, obj.first_name]))
        if not name:
            name = obj.username
        return name

    def available_replacement_device(self):
        qs = self.fields['replacement_device'].queryset.filter(
            Q(booking__isnull=True) | Q(booking=self.instance))
        return qs

    def change_field_attribute(self, field_name, attribute, value):
        field = self.fields.get(field_name)
        if field:
            setattr(field, attribute, value)
        return field

    def change_fields_attribute(self, fields_name, attribute, value):
        fields = []
        for field_name in fields_name:
            fields.append(
                self.change_field_attribute(field_name, attribute, value))
        return fields


class BookingForm(BaseBookingForm):
    class Meta:
        model = Booking

        fields = (
            'done_work',
            'guarantee',
            'master',
            'replacement_device',
        )

        widgets = {
            'done_work': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.state == State.WORKING:
            self.change_fields_attribute(['guarantee', 'master', 'done_work'],
                                         'disabled', True)

    def clean_done_work(self):
        def price_to_int(obj):
            if 'price' in obj:
                obj['price'] = int(obj['price'])
            return obj
        data = self.cleaned_data['done_work']
        if data:
            data = list(map(lambda obj: price_to_int(obj), data))
        transition = self.data.get('transition')
        if self.instance.state == State.WORKING:
            if transition == 'ready' and not data:
                raise forms.ValidationError(
                    'Необходимо заполнить выполненную работу')
        return data
