from django import forms
from .models import Article

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'
    format = 'DATETIME_FORMAT'


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'publish']
        widgets = {'publish': DateTimeInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control form-control-sm',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
