from django import forms
from django.http import request
from .models import Faq

class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ['category', 'question', 'answer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
