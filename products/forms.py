from django import forms
from .models import Product

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
