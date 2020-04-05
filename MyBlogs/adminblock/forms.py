from django import forms

from .models import Admin
class AdminRegistration(forms.ModelForm):
    class Meta:
        model=Admin
        fields = {
            'admin_name','avatar','description','password'
        }
        widgets = {
            'admin_name': forms.TextInput(),
            'avatar': forms.TextInput(),
            'description': forms.Textarea(),
            'password': forms.PasswordInput()
        }
        labels = {
            'admin_name': 'Name',
            'avatar': 'Avatar',
            'description': 'Description',
            'password': 'Password'
        }