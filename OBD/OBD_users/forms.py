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

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white shadow-sm hover:shadow-md',
                'placeholder': 'Nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white shadow-sm hover:shadow-md',
                'placeholder': 'correo@ejemplo.com'
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-blue-600 bg-white border-2 border-gray-300 rounded focus:ring-blue-500 focus:ring-2 transition-all duration-200'
            }),
            'is_superuser': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-red-600 bg-white border-2 border-gray-300 rounded focus:ring-red-500 focus:ring-2 transition-all duration-200'
            })
        }
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'is_staff': 'Es staff',
            'is_superuser': 'Es superusuario'
        }
        help_texts = {
            'username': 'Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_',
            'email': 'Ingresa una dirección de correo válida',
            'is_staff': 'Status de STAFF',
            'is_superuser': 'status de ADMINISTRADOR'
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'displayname', 'info', 'image']
        widgets = {
            'role': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200 bg-white shadow-sm hover:shadow-md'
            }),
            'displayname': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200 bg-white shadow-sm hover:shadow-md',
                'placeholder': 'Nombre para mostrar'
            }),
            'info': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200 bg-white shadow-sm hover:shadow-md resize-none',
                'placeholder': 'Información adicional sobre el usuario...',
                'rows': 4
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200 bg-white shadow-sm hover:shadow-md file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100',
                'accept': 'image/*'
            })
        }
        labels = {
            'role': 'Rol del usuario',
            'displayname': 'Nombre a mostrar',
            'info': 'Información adicional',
            'image': 'Imagen de perfil'
        }
        help_texts = {
            'role': 'Selecciona el rol que tendrá este usuario',
            'displayname': 'Nombre que se mostrará públicamente',
            'info': 'Información adicional o biografía del usuario',
            'image': 'Imagen de perfil (formatos: JPG, PNG)'
        }