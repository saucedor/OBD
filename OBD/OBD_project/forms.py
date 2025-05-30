from django import forms
from .models import MensajeContacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 px-3 py-2 rounded',
                'placeholder': 'Tu nombre'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 px-3 py-2 rounded',
                'placeholder': 'tucorreo@example.com'
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 px-3 py-2 rounded',
                'rows': 4,
                'placeholder': 'Escribe tu mensaje...'
            }),
        }
