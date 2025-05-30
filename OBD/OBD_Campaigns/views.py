from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from .models import Campana, Item
from django.shortcuts import get_object_or_404, render
from .forms import CampanaForm, ItemForm    
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def vista_campanas(request):
    campanas = Campana.objects.order_by('-fecha_creacion_campana')
    es_admin = request.user.is_superuser
    return render(request, 'OBD_Campaigns/campana.html', {
        'campanas': campanas,
        'es_admin': es_admin
    })

@login_required
def detalle_campana(request, pk):
    campana = get_object_or_404(Campana, pk=pk)
    return render(request, 'OBD_Campaigns/campana.html', {
        'campana': campana
    })

@login_required
def borrar_confirmacion_campana(request, pk):
    campana = get_object_or_404(Campana, pk=pk)
    return render(request, 'OBD_Campaigns/partial_confirm_delete.html', {
        'campana': campana
    })

@csrf_exempt
@require_http_methods(["DELETE"])
def borrar_campana(request, pk):
    campana = get_object_or_404(Campana, pk=pk)
    campana.delete()
    return HttpResponse("")  # Devuelve string vacío en lugar de 204

@login_required
@user_passes_test(lambda u: u.is_superuser)
def crear_campana(request):
    if request.method == 'POST':
        form = CampanaForm(request.POST, request.FILES)
        if form.is_valid():
            campana = form.save(commit=False)
            campana.administrador = request.user
            campana.save()
            form.save_m2m()
            return redirect('vista_campanas')
    else:
        form = CampanaForm()
    return render(request, 'OBD_Campaigns/form_campana.html', {'form': form})

@login_required
def detalle_campana(request, pk):
    campana = get_object_or_404(Campana, pk=pk)
    return render(request, 'OBD_Campaigns/detalle_campana.html', {
        'campana': campana
    })


def items_campana_view(request, campana_id):
    campana = get_object_or_404(Campana, id=campana_id)
    productos = Item.objects.filter(campana=campana)

    return render(request, 'OBD_Campaigns/items_campana.html', {
        'campana': campana,
        'productos': productos
    })

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def crear_item(request, campana_id):
    campana = get_object_or_404(Campana, id=campana_id)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.campana = campana
            item.save()
            return redirect('items_campana', campana_id=campana.id)
    else:
        form = ItemForm()

    return render(request, 'OBD_Campaigns/form_item.html', {
        'form': form,
        'campana': campana
    })
