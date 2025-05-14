from django.forms import ModelForm 
from django import forms 
from .models import Profile 
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm


class ProfileForm(ModelForm):
    class Meta:
        model = Profile 
        exclude = ['user', 'role']
        widgets = {
            'image': forms.FileInput(),
            'displayname': forms.TextInput(attrs={'placeholder': 'Anadir Nombre'}),
            'info': forms.Textarea(attrs={'rows':3, 'placeholder': 'Anadir Informacion'})
        }

class CustomSignupForm(SignupForm):
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        label="Tipo de cuenta",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def save(self, request):
        user = super().save(request)
        role = self.cleaned_data['role']

        # El Profile ya fue creado por la señal, solo actualizamos el rol
        profile = user.profile
        profile.role = role
        profile.save()

        return user

class EmailForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta: 
        model = User
        fields = ['email']