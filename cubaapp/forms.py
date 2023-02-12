from django import forms
from django.forms import ModelForm

from .models import *

class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=200, widget= forms.Textarea(attrs={'placeholder':'Enter new task here. . .'}))
    class Meta:
        model = User
        fields = '__all__'
        
        
class CameraForm(forms.ModelForm):
    camera_name = forms.CharField(max_length=100)
    ip_address = forms.CharField(max_length=200, required=False)
    camera_details = forms.URLField()
    other_details = forms.FloatField()
    
    class Meta:
        model = Camera
        fields = '__all__'