from django import forms

from crm.models import Booking, State

from pipeline.forms import PipelineFormMedia


class BaseBookingForm(forms.ModelForm):
    """
    Базовый класс формы заявки
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['master'].label_from_instance = self.master_label

    @staticmethod
    def master_label(obj):
        """
        Показываем фамилию и имя вместо логина
        """
        name = ' '.join(filter(None, [obj.last_name, obj.first_name]))
        if not name:
            name = obj.username
        return name


class BookingForm(BaseBookingForm):
    class Meta:
        model = Booking

        fields = (
            'done_work',
            'guarantee',
            'master',
        )

        widgets = {
            'done_work': forms.HiddenInput,
        }

    class Media(PipelineFormMedia):
        js_packages = (
            'marionette',
            'jobs',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.state == State.WORKING:
            self.fields['guarantee'].disabled = True
            self.fields['master'].disabled = True

    def clean_done_work(self):
        data = self.cleaned_data['done_work']
        transition = self.data.get('transition')
        if self.instance.state == State.WORKING:
            if transition == 'ready' and not data:
                raise forms.ValidationError(
                    'Необходимо заполнить выполненную работу')
        else:
            data = self.instance.done_work
        return data
