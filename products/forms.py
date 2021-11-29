from django import forms
from .models import Product, PurchaseItem, PurchaseOrder
from django.contrib.auth.models import User
from django.utils.encoding import smart_text

class ProductForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    class Meta:
        model = Product
        fields = ['name', 'type', 'low_alert_level', 'active']

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


# purchase order forms

class UserFullnameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return smart_text(obj.get_full_name())

class DateInput(forms.DateInput):
    input_type = 'date'

class PurchaseOrderForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    # user = UserFullnameChoiceField(queryset=User.objects.filter(is_active=True).exclude(first_name__exact='').order_by('first_name'))

    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'date']
        widgets = {'date': DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        

class PurchaseItemForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    class Meta:
        model = PurchaseItem
        fields = ['product', 'price_each', 'purchased_quantity', 'received_quantity']

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
