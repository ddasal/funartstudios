from django import forms
from .models import TimeOffRequest

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'
    # format = 'I:M p'

class TimeOffForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    class Meta:
        model = TimeOffRequest
        fields = ['start_date', 'start_time', 'end_date', 'end_time', 'notes']
        widgets = {'start_date': DateInput(), 'start_time': TimeInput(), 'end_date': DateInput(), 'end_time': TimeInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        # self.fields['active'].widget.attrs.update({'class': 'form-check'})

