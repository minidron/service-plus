from django import forms

from crm.models import Booking, State

from pipeline.forms import PipelineFormMedia


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking

        fields = (
            'done_work',
        )

        widgets = {
            'done_work': forms.HiddenInput,
        }

    class Media(PipelineFormMedia):
        js_packages = (
            'marionette',
            'jobs',
        )

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
