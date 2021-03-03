from django import forms
from django.forms import ModelForm
from .models import *

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control mb-2', 'placeholder': 'What is happening on Middle Earth?', 'id': 'postBody', 'rows': '5'})
        }

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control mb-2', 'placeholder': 'Write something about yourself', 'rows': '5'}),
            'avatar': forms.URLInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Share your good profile'})
        }


