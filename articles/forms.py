from django import forms
from django.http import request
from .models import Article, Comment

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'publish']
        widgets = {'publish': DateTimeInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )

class CommentForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control form-control-sm',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        self.fields['comment'].widget.attrs.update({'rows': '3'})
