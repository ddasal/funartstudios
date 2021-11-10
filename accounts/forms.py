from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )



class RegisterForm(UserCreationForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password1' ,'password2' )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )

class UserProfileForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    class Meta:
        model = UserProfile
        fields = ['phone_mobile', 'phone_home', 'address', 'city', 'state', 'zip', 'emergency_contact_name_1', 'emergency_contact_number_1', 'emergency_contact_email_1', 'emergency_contact_name_2', 'emergency_contact_number_2', 'emergency_contact_email_2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        # self.fields['active'].widget.attrs.update({'class': 'form-check'})
