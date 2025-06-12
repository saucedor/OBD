from django import forms
from django.contrib.auth.models import User
from .models import Campana, Item, ArchivoLive

class CampanaForm(forms.ModelForm):
    class Meta:
        model = Campana
        fields = [
            'nombre_campana',
            'nombre_empresa',
            'foto',
            'contacto_dueno',
            'descripcion_campana',
            'estado',
            'cliente',
            'vendedores'
        ]
        
        widgets = {
            'nombre_campana': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 focus:bg-white',
                'placeholder': 'Nombre de la campaña'
            }),
            'nombre_empresa': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 focus:bg-white',
                'placeholder': 'Nombre de la empresa'
            }),
            'contacto_dueno': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 focus:bg-white',
                'placeholder': 'Contacto del dueño'
            }),
            'descripcion_campana': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 focus:bg-white resize-none',
                'placeholder': 'Describe los objetivos y detalles de la campaña...'
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 focus:bg-white'
            }),
            'foto': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-dashed border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-gray-50 focus:bg-white',
                'accept': 'image/*'
            }),
            'cliente': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 focus:bg-white'
            }),
            'vendedores': forms.SelectMultiple(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 focus:bg-white',
                'size': '5'
            }),
        }
        
        labels = {
            'nombre_campana': 'Nombre de la Campaña',
            'nombre_empresa': 'Empresa',
            'foto': 'Imagen de la Campaña',
            'contacto_dueno': 'Contacto del Dueño',
            'descripcion_campana': 'Descripción',
            'estado': 'Estado de la Campaña',
            'cliente': 'Cliente Asignado',
            'vendedores': 'Staff Asignado'
        }
        
        help_texts = {
            'nombre_campana': 'Ingresa un nombre descriptivo para la campaña',
            'nombre_empresa': 'Nombre de la empresa cliente',
            'foto': 'Sube una imagen representativa de la campaña (opcional)',
            'contacto_dueno': 'Información de contacto del responsable',
            'descripcion_campana': 'Describe los objetivos, alcance y detalles de la campaña',
            'estado': 'Estado actual de la campaña (por defecto: Activo)',
            'cliente': 'Selecciona el cliente responsable de esta campaña',
            'vendedores': 'Selecciona uno o más miembros del staff para esta campaña'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar usuarios para cliente (no staff ni superuser)
        self.fields['cliente'].queryset = User.objects.filter(
            is_staff=False,
            is_superuser=False,
            is_active=True
        )
        self.fields['cliente'].empty_label = "Selecciona un cliente"
        
        # Filtrar vendedores (solo staff, no superuser)
        self.fields['vendedores'].queryset = User.objects.filter(
            is_staff=True,
            is_superuser=False,
            is_active=True
        )
        
        # Establecer estado por defecto
        if not self.instance.pk:
            self.fields['estado'].initial = 'activo'

    def clean_nombre_campana(self):
        nombre = self.cleaned_data.get('nombre_campana')
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre de la campaña debe tener al menos 3 caracteres.')
        return nombre

    def clean_nombre_empresa(self):
        empresa = self.cleaned_data.get('nombre_empresa')
        if len(empresa) < 2:
            raise forms.ValidationError('El nombre de la empresa debe tener al menos 2 caracteres.')
        return empresa
    

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nombre_producto', 'desc_producto', 'cantidad_disponible', 'cantidad_vendida', 'costo_unitario', 'foto']
        
        widgets = {
            'nombre_producto': forms.TextInput(attrs={
                'class': 'form-input transition-all duration-300 ease-in-out border-2 border-gray-200 rounded-lg px-4 py-3 bg-gray-50 focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-blue-100',
                'placeholder': 'Ingresa el nombre del producto'
            }),
            
            'desc_producto': forms.Textarea(attrs={
                'class': 'form-textarea transition-all duration-300 ease-in-out border-2 border-gray-200 rounded-lg px-4 py-3 bg-gray-50 focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-blue-100 resize-none',
                'rows': 4,
                'placeholder': 'Describe las características principales del producto'
            }),
            
            'cantidad_disponible': forms.NumberInput(attrs={
                'class': 'form-number transition-all duration-300 ease-in-out border-2 border-gray-200 rounded-lg px-4 py-3 bg-gray-50 focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-blue-100',
                'min': '0',
                'placeholder': '0'
            }),
            
            'cantidad_vendida': forms.NumberInput(attrs={
                'class': 'form-number transition-all duration-300 ease-in-out border-2 border-gray-200 rounded-lg px-4 py-3 bg-gray-50 focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-blue-100',
                'min': '0',
                'placeholder': '0'
            }),
            
            'costo_unitario': forms.NumberInput(attrs={
                'class': 'form-number transition-all duration-300 ease-in-out border-2 border-gray-200 rounded-lg px-4 py-3 bg-gray-50 focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-blue-100',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            
            'foto': forms.ClearableFileInput(attrs={
                'class': 'form-file transition-all duration-300 ease-in-out border-2 border-gray-200 rounded-lg px-4 py-3 bg-gray-50 focus:border-blue-500 focus:bg-white focus:outline-none cursor-pointer',
                'accept': 'image/*'
            })
        }
        
        labels = {
            'nombre_producto': 'Nombre del producto',
            'desc_producto': 'Descripción del producto',
            'cantidad_disponible': 'Cantidad disponible',
            'cantidad_vendida': 'Cantidad vendida',
            'costo_unitario': 'Costo unitario',
            'foto': 'Foto del producto'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Agregar clases adicionales para campos específicos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'data-field': field_name
            })
            
            # Configuración específica por tipo de campo
            if isinstance(field.widget, forms.NumberInput):
                field.widget.attrs.update({
                    'inputmode': 'numeric'
                })
            
            if field_name == 'foto':
                field.widget.attrs.update({
                    'onchange': 'handleFileSelect(this)'
                })

class ArchivoLiveForm(forms.ModelForm):
    class Meta:
        model = ArchivoLive
        fields = ['nombre_corto', 'archivo', 'campana']
        widgets = {
            'nombre_corto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre descriptivo del archivo live'
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            }),
        }
        labels = {
            'nombre_corto': 'Nombre del Archivo',
            'archivo': 'Archivo de Video',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CSVUploadForm(forms.Form):
    archivo_csv = forms.FileField(
        label='Archivo CSV',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        })
    )

class CSVComentarioForm(forms.Form):
    csv_file = forms.FileField(
        label="Archivo CSV",
        help_text="Sube un archivo .csv con los comentarios",
        widget=forms.FileInput(attrs={
            "accept": ".csv",
            "class": "text-sm text-gray-700"
        })
    )