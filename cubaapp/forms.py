from django import forms
from django.forms import ModelForm

from .models import *

class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=200, widget= forms.Textarea(attrs={'placeholder':'Enter new task here. . .'}))
    class Meta:
        model = User
        fields = '__all__'