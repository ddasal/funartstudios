from django.conf import settings
from django.contrib.auth.models import User
from django.utils.encoding import smart_text
from django import forms

from products.models import Product
from .models import AdminPay, Event, EventCustomer, EventStaff, EventTip, EventImages

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'
    # format = 'I:M p'

class EventForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    class Meta:
        model = Event
        fields = ['title', 'date', 'time', 'length', 'type', 'active']
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
        fields = ['user', 'staff_notes', 'role', 'hours', 'prepaint_product', 'prepaint_qty', 'event_product', 'event_qty']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control form-control-sm',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        self.fields['staff_notes'].widget.attrs.update({"placeholder": 'As needed, please enter any notes for management in this field'})
        self.fields['staff_notes'].widget.attrs.update({"rows": '4'})
        self.fields['prepaint_product'].queryset = self.fields['prepaint_product'].queryset.exclude(active=False)
        self.fields['event_product'].queryset = self.fields['event_product'].queryset.exclude(active=False)

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


class EventTipForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    class Meta:
        model = EventTip
        fields = ['tip_amount', 'stage_split']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control form-control-sm',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )

class EventImageForm(forms.ModelForm):
    class Meta:
        model = EventImages
        fields = ['title', 'upload']


class AdminPayForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    user = UserFullnameChoiceField(queryset=User.objects.filter(is_active=True).exclude(first_name__exact='').order_by('first_name'))

    class Meta:
        model = AdminPay
        fields = ['user', 'admin_pay', 'note']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control form-control-sm',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
