from django.shortcuts import render, redirect
from .forms import ContactoForm
from OBD_Campaigns.models import Campana

# Create your views here.

def home_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            campanas_activas = Campana.objects.filter(
                estado='activo'
            ).order_by('-fecha_creacion_campana')[:6]
        else:
            campanas_activas = Campana.objects.filter(
                estado='activo'
            ).filter(
                cliente=request.user
            ) | Campana.objects.filter(
                estado='activo',
                vendedores=request.user
            )
            campanas_activas = campanas_activas.distinct().order_by('-fecha_creacion_campana')[:6]
    else:
        campanas_activas = []

    return render(request, 'OBD_project/home.html', {
        'campanas_activas': campanas_activas
    })

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'OBD_project/contacto.html', {
                'form': ContactoForm(), 
                'exito': True
            })
    else:
        form = ContactoForm()
    return render(request, 'OBD_project/contacto.html', {'form': form})

def about(request):
    return render(request, 'OBD_project/about.html', {
        
    })

