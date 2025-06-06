from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from .models import Campana, Item, ArchivoLive, Comentario
from django.shortcuts import get_object_or_404, render
from .forms import CampanaForm, ItemForm, ArchivoLiveForm, CSVUploadForm   
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.urls import reverse
from django.contrib import messages
import csv

# Dashboard de campañas
@login_required
def vista_campanas(request):
    campanas = Campana.objects.order_by('-fecha_creacion_campana')
    es_admin = request.user.is_superuser
    return render(request, 'OBD_Campaigns/campana.html', {
        'campanas': campanas,
        'es_admin': es_admin
    })

#Vista a una campaña específica
@login_required
def detalle_campana(request, pk):
    campana = get_object_or_404(Campana, pk=pk)
    return render(request, 'OBD_Campaigns/campana.html', {
        'campana': campana
    })

# Vista para confirmar la eliminación de una campaña
@login_required
def borrar_confirmacion_campana(request, pk):
    campana = get_object_or_404(Campana, pk=pk)
    return render(request, 'OBD_Campaigns/partial_confirm_delete.html', {
        'campana': campana
    })

# Vista para eliminar una campaña
@csrf_exempt
@require_http_methods(["DELETE"])
def borrar_campana(request, pk):
    campana = get_object_or_404(Campana, pk=pk)
    campana.delete()
    return HttpResponse("")  # Devuelve string vacío en lugar de 204

# formulario para crear una nueva campaña
@never_cache
@require_http_methods(["GET", "POST"])
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
            
            # Añadir mensaje de éxito
            messages.success(request, f'Campaña "{campana.nombre_campana}" creada exitosamente.')
            
            # Patrón Post-Redirect-Get: redirigir después del POST exitoso
            return redirect(reverse('vista_campanas'))
    else:
        form = CampanaForm()
    
    # Añadir headers anti-cache en la respuesta
    response = render(request, 'OBD_Campaigns/form_campana.html', {'form': form})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@login_required
def detalle_campana(request, pk):
    campana = get_object_or_404(Campana, pk=pk)
    productos = Item.objects.filter(campana=campana)
    archivos_live = ArchivoLive.objects.filter(campana=campana).order_by('-fecha_subida')
    return render(request, 'OBD_Campaigns/detalle_campana.html', {
        'campana': campana,
        'productos': productos,
        'archivos_live': archivos_live,
    })

# Vista de los ítems de una campaña
def items_campana_view(request, campana_id):
    campana = get_object_or_404(Campana, id=campana_id)
    productos = Item.objects.filter(campana=campana)

    return render(request, 'OBD_Campaigns/items_campana.html', {
        'campana': campana,
        'productos': productos
    })

# formulario para crear un nuevo ítem en una campaña
@never_cache
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

# Vista de archivos live de una campaña
@login_required
def archivolive_campana(request, campana_id):
    campana = get_object_or_404(Campana, id=campana_id)
    archivos = ArchivoLive.objects.filter(campana=campana).order_by('-fecha_subida')
    return render(request, 'OBD_Campaigns/archivolive_campana.html', {
        'campana': campana,
        'archivos': archivos
    })

# Formulario para crear un nuevo archivo live en una campaña
@never_cache
@login_required
@user_passes_test(lambda u: u.is_superuser or u.profile.role == 'vendedor')
def crear_archivolive(request, campana_id):
    campana = get_object_or_404(Campana, id=campana_id)
    if request.method == 'POST':
        form = ArchivoLiveForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save(commit=False)
            archivo.usuario = request.user
            archivo.campana = campana
            archivo.save()
            return redirect('archivolive_campana', campana_id=campana.id)
    else:
        form = ArchivoLiveForm(initial={'campana': campana})
    return render(request, 'OBD_Campaigns/form_archivolive.html', {
        'form': form,
        'campana': campana
    })

# formulario para importar ítems desde un archivo CSV
@login_required
def importar_items_csv(request, pk):
    campana = get_object_or_404(Campana, pk=pk)

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.cleaned_data['archivo_csv']
            decoded = archivo.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded)

            for row in reader:
                Item.objects.create(
                    nombre_producto=row['nombre_producto'],
                    desc_producto=row.get('desc_producto', ''),
                    cantidad_disponible=int(row['cantidad_disponible']),
                    cantidad_vendida=int(row.get('cantidad_vendida', 0)),
                    costo_unitario=float(row['costo_unitario']),
                    campana=campana
                )
            messages.success(request, "Ítems cargados exitosamente.")
            return redirect('items_campana', campana_id=pk)
    else:
        form = CSVUploadForm()

    return render(request, 'OBD_Campaigns/form_cargar_items.html', {
        'form': form,
        'campana': campana
    })

# formulario para editar una item 
@login_required
def editar_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponse('<script>window.location.reload()</script>')
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'OBD_Campaigns/includes/form_editar_item.html', {
        'form': form,
        'item': item  
    })

# formulario para editar un archivo live
@login_required
def editar_archivo_live(request, archivo_id):
    archivo = get_object_or_404(ArchivoLive, id=archivo_id)
    if request.method == 'POST':
        form = ArchivoLiveForm(request.POST, request.FILES, instance=archivo)
        if form.is_valid():
            form.save()
            return HttpResponse('<script>window.location.reload()</script>')
    else:
        form = ArchivoLiveForm(instance=archivo)
    
    return render(request, 'OBD_Campaigns/includes/form_editar_archivo_live.html', {
        'form': form,
        'archivo': archivo
    })

# vista para eliminar un archivo live
@login_required
def eliminar_archivo_live(request, archivo_id):
    archivo = get_object_or_404(ArchivoLive, id=archivo_id)
    archivo.delete()
    return HttpResponse('<script>window.location.reload()</script>')

# vista para eliminar un item
@login_required
def eliminar_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return HttpResponse('<script>window.location.reload()</script>')

# Vista para ver comentarios por campaña
@login_required
def comentarios_por_campana(request, campania_id):
    campana = get_object_or_404(Campana, id=campania_id)
    comentarios = Comentario.objects.filter(campania=campana).order_by('-fecha')

    return render(request, 'comentarios/comentarios_campana.html', {
        'campana': campana,
        'comentarios': comentarios
    })