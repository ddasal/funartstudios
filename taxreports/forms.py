from django.utils.encoding import smart_text
from django import forms

from .models import TaxReport

class DateInput(forms.DateInput):
    input_type = 'date'

class UserFullnameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return smart_text(obj.get_full_name())


class ReportForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    class Meta:
        model = TaxReport
        fields = ['start_date', 'end_date']
        widgets = {'start_date': DateInput(), 'end_date': DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
