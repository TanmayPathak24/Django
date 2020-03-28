from django import forms

from .models import Blog
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = {
            'id','author','title','content'
        }
        widgets = {
            'id': forms.TextInput(),
            'author': forms.TextInput(),
            'title': forms.TextInput(),
            'content': forms.Textarea()
        }
        labels = {
            'author':'Author',
            'title':'Title',
            'content':'Content (Max: 5000 characters)'
        }