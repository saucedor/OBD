from django.forms import ModelForm 
from django import forms 
from .models import Profile 

class ProfileForm(ModelForm):
    class Meta:
        model = Profile 
        exclude = ['user', 'role']
        widgets = {
            'image': forms.FileInput(),
            'displayname': forms.TextInput(attrs={'placeholder': 'Anadir Nombre'}),
            'info': forms.Textarea(attrs={'rows':3, 'placeholder': 'Anadir Informacion'})
        }

