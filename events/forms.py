from django.conf import settings
from django.contrib.auth.models import User
from django.utils.encoding import smart_text
from django import forms

from products.models import Product
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
        fields = ['title', 'date', 'time', 'length', 'type', 'credit_tips', 'active']
        widgets = {'date': DateInput(), 'time': TimeInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        self.fields['active'].widget.attrs.update({'class': 'form-check'})


class UserFullnameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return smart_text(obj.get_full_name())

class EventStaffForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    user = UserFullnameChoiceField(queryset=User.objects.filter(is_active=True).exclude(first_name__exact='').order_by('first_name'))

    class Meta:
        model = EventStaff
        fields = ['user', 'role', 'hours', 'prepaint_product', 'prepaint_qty', 'event_product', 'event_qty']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control form-control-sm',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        self.fields['prepaint_product'].queryset = self.fields['prepaint_product'].queryset.exclude(active=False)
        self.fields['event_product'].queryset = self.fields['event_product'].queryset.exclude(active=False)
        # self.fields['to_user'].queryset = self.fields['to_user'].queryset.exclude(id=current_user.id)


class EventCustomerForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    class Meta:
        model = EventCustomer
        fields = ['quantity', 'price', 'type', 'product', 'per_customer_qty']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control form-control-sm',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        self.fields['product'].queryset = self.fields['product'].queryset.exclude(active=False)
