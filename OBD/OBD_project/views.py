from django.shortcuts import render, redirect
from .forms import ContactoForm
from OBD_Campaigns.models import Campana
from django.utils.timezone import now, timedelta
from django.db.models import Count, Q
from OBD_Campaigns.models import Comentario, Tarea
from django.contrib.auth.models import User
from OBD_users.models import Profile

# Create your views here.

def home_view(request):
    campanas_activas = []
    tareas = Comentario.objects.none()
    comentarios = Comentario.objects.none()

    if request.user.is_authenticated:
        if request.user.is_superuser:
            campanas = Campana.objects.all()
            tareas = Tarea.objects.all()
        else:
            campanas = Campana.objects.filter(
                Q(cliente=request.user) | Q(vendedores=request.user)
            ).distinct()
            tareas = Tarea.objects.filter(asignados=request.user)

        campanas_activas = campanas.filter(estado='activo').order_by('-fecha_creacion_campana')[:6]
        comentarios = Comentario.objects.filter(campania__in=campanas)

        context = {
            'campanas_activas': campanas_activas,
            'estadisticas_estado': campanas.values("estado").annotate(total=Count("id")),
            'tareas_completadas': tareas.filter(completado=True).count(),
            'tareas_pendientes': tareas.filter(completado=False).count(),
            # 'ranking_staff': [],
            'comentarios_por_campana': comentarios.values("campania__nombre_campana").annotate(total=Count("id")),
            'campanas_mes': campanas.filter(
                fecha_creacion_campana__gte=now() - timedelta(days=30)
            ).count(),
            'campanas_recientes': campanas.filter(
                fecha_creacion_campana__gte=now() - timedelta(days=30)
            ).order_by("-fecha_creacion_campana")[:5],
        }
    else:
        context = {
            'campanas_activas': [],
            'estadisticas_estado': [],
            'tareas_completadas': 0,
            'tareas_pendientes': 0,
            'ranking_staff': [],
            'comentarios_por_campana': [],
            'campanas_mes': 0,
            'campanas_recientes': [],
        }

    return render(request, 'OBD_project/home.html', context)

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

