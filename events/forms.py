from django.conf import settings
from django.contrib.auth.models import User
from django.utils.encoding import smart_text
from django import forms
from .models import Event, EventCustomer, EventStaff

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class EventForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    class Meta:
        model = Event
        fields = ['title', 'date', 'time', 'length', 'type', 'credit_tips']
        widgets = {'date': DateInput(), 'time': TimeInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                # "placeholder": f'Event {str(field)}',
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        

class UserFullnameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return smart_text(obj.get_full_name())

class EventStaffForm(forms.ModelForm):
    user = UserFullnameChoiceField(queryset=User.objects.filter(is_active=True).exclude(first_name__exact='').order_by('first_name'))

    class Meta:
        model = EventStaff
        fields = ['user', 'role', 'hours']


class EventCustomerForm(forms.ModelForm):

    class Meta:
        model = EventCustomer
        fields = ['quantity', 'type']