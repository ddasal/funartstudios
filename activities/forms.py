from django.conf import settings
from django.contrib.auth.models import User
from django.utils.encoding import smart_text
from django import forms

from products.models import Product
from .models import ActivityAdminPay, Activity, ActivityCustomer, ActivityStaff, ActivityTip, ActivityImages

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'
    # format = 'I:M p'

class ActivityForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    class Meta:
        model = Activity
        fields = ['type', 'date', 'time', 'hours', 'notes', 'active']
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

class ActivityStaffForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    user = UserFullnameChoiceField(queryset=User.objects.filter(is_active=True).exclude(first_name__exact='').order_by('first_name'))

    class Meta:
        model = ActivityStaff
        fields = ['user', 'activity_product', 'activity_qty']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control form-control-sm',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        # self.fields['prepaint_product'].queryset = self.fields['prepaint_product'].queryset.exclude(active=False)
        self.fields['activity_product'].queryset = self.fields['activity_product'].queryset.exclude(active=False)

class ActivityCustomerForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    class Meta:
        model = ActivityCustomer
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


class ActivityTipForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    class Meta:
        model = ActivityTip
        fields = ['tip_amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control form-control-sm',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )

class ActivityImageForm(forms.ModelForm):
    class Meta:
        model = ActivityImages
        fields = ['title', 'upload']


class ActivityAdminPayForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    user = UserFullnameChoiceField(queryset=User.objects.filter(is_active=True).exclude(first_name__exact='').order_by('first_name'))

    class Meta:
        model = ActivityAdminPay
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
