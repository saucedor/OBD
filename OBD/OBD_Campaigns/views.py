from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods, require_POST
from django.shortcuts import render, redirect
from .models import Campana, Item, ArchivoLive, Comentario, Tarea 
from django.shortcuts import get_object_or_404, render
from .forms import CampanaForm, ItemForm, ArchivoLiveForm, CSVUploadForm, CSVComentarioForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.urls import reverse
from django.contrib import messages
import csv
import datetime
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from io import TextIOWrapper
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db import models
from OBD_users.models import Profile

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
    comentarios = Comentario.objects.filter(campania=campana).order_by('-fecha')
    return render(request, 'OBD_Campaigns/detalle_campana.html', {
        'campana': campana,
        'productos': productos,
        'archivos_live': archivos_live,
        'comentarios': comentarios,
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

    return render(request, 'OBD_Campaigns/comentarios_campana.html', {
        'campana': campana,
        'comentarios': comentarios
    })

# Vista para importar comentarios desde un CSV
@login_required
def subir_csv_comentarios(request, campania_id):
    campana = get_object_or_404(Campana, id=campania_id)

    if request.method == "POST":
        form = CSVComentarioForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                csv_file = form.cleaned_data["csv_file"]
                wrapper = TextIOWrapper(csv_file.file, encoding="utf-8", newline='')
                reader = csv.reader(wrapper)

                # Saltar las primeras 5 filas basura
                for _ in range(5):
                    next(reader)

                headers = next(reader)  # fila real de encabezados

                for row in reader:
                    try:
                        perfil_nombre = row[2].strip()
                        perfil_id = row[3].strip()
                        fecha_str = row[4].strip()
                        texto = row[5].strip()
                        fuente_url = row[6].strip()
                        perfil_url = f"https://facebook.com/{perfil_id}" if perfil_id else ""

                        fecha_parseada = parse_datetime(fecha_str)
                        if fecha_parseada is not None:
                            fecha = make_aware(fecha_parseada)
                        else:
                            fecha = datetime.datetime.now()

                        if perfil_nombre or texto:
                            Comentario.objects.create(
                                campania=campana,
                                perfil_nombre=perfil_nombre,
                                perfil_url=perfil_url,
                                perfil_id=perfil_id,
                                texto=texto,
                                fuente_url=fuente_url,
                                fecha=fecha
                            )
                    except Exception as fila_error:
                        print(f"❌ Error en fila: {fila_error}")

                messages.success(request, "Comentarios importados correctamente.")
                return redirect("comentarios_campana", campania_id=campana.id)

            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {e}")

    else:
        form = CSVComentarioForm()

    return render(request, "OBD_Campaigns/form_cargar_comentarios.html", {
        "form": form,
        "campana": campana
    })

# Vista para gestionar las funciones de los comentarios
@login_required
@require_POST
def procesar_comentarios(request, campania_id):
    accion = request.POST.get("accion")
    comentarios_ids = request.POST.getlist("comentarios_seleccionados")

    if not comentarios_ids:
        # podrías agregar un mensaje aquí
        return redirect("comentarios_campana", campania_id=campania_id)

    if accion == "borrar":
        Comentario.objects.filter(id__in=comentarios_ids).delete()
    elif accion == "asignar":
        # Placeholder: redirige a una vista de asignación, o implementa la lógica directamente aquí
        request.session['comentarios_a_asignar'] = comentarios_ids
        return redirect("asignar_tareas", campania_id=campania_id)

    return redirect("comentarios_campana", campania_id=campania_id)

# Vista para asignar tareas a comentarios
@login_required
def asignar_tareas(request, campania_id):
    campana = get_object_or_404(Campana, id=campania_id)
    comentario_ids = request.session.get('comentarios_a_asignar', [])

    comentarios = Comentario.objects.filter(id__in=comentario_ids)
    vendedores = User.objects.filter(is_staff=True, is_superuser=False).order_by('username')

    if request.method == "POST":
        seleccionados = request.POST.getlist("comentarios")
        vendedores_ids = request.POST.getlist("vendedores")
        tipo = request.POST.get("tipo", "responder")
        descripcion = request.POST.get("descripcion", "")

        for comentario_id in seleccionados:
            comentario = Comentario.objects.get(id=comentario_id)
            tarea = Tarea.objects.create(comentario=comentario, tipo=tipo, descripcion=descripcion)
            tarea.asignados.set(vendedores_ids)

        request.session.pop('comentarios_a_asignar', None)
        return redirect("comentarios_campana", campania_id=campania_id)

    return render(request, "OBD_Campaigns/asignar_tareas.html", {
        "campana": campana,
        "comentarios": comentarios,
        "vendedores": vendedores
    })


# Vista para listar todos los comentarios
@login_required
def lista_comentarios(request):
    user = request.user

    if user.is_superuser:
        comentarios = Comentario.objects.all()
    elif user.is_staff:
        # Filtra campañas donde el usuario es parte del staff asignado
        campañas_asignadas = Campana.objects.filter(vendedores=user)
        comentarios = Comentario.objects.filter(campana__in=campañas_asignadas)
    else:
        comentarios = Comentario.objects.none()  # Usuario normal no ve nada

    # Filtros GET
    usuario = request.GET.get("usuario")
    contenido = request.GET.get("contenido")
    fecha = request.GET.get("fecha")
    campana_id = request.GET.get("campana")

    if usuario:
        comentarios = comentarios.filter(perfil_nombre__icontains=usuario)
    if contenido:
        comentarios = comentarios.filter(texto__icontains=contenido)
    if fecha:
        comentarios = comentarios.filter(fecha_creacion__date=fecha)
    if campana_id:
        comentarios = comentarios.filter(campania__id=campana_id)

    campanas = Campana.objects.all() if user.is_superuser else campañas_asignadas

    return render(request, "OBD_Campaigns/comentarios.html", {
        "comentarios": comentarios,
        "campanas": campanas,
    })

# Vista de tareas para staff
@login_required
def vista_tareas_staff(request):
    if request.user.is_staff and not request.user.is_superuser:
        tareas = Tarea.objects.filter(asignados=request.user)
        campanas = Campana.objects.filter(staff=request.user)
        return render(request, 'OBD_Campaigns/tareas_staff.html', {
            'tareas': tareas,
            'campanas': campanas
        })
    
# Vista de tareas para superusuarios
@login_required
def vista_tareas_superuser(request):
    if request.user.is_superuser:
        staff_profiles = Profile.objects.filter(user__is_staff=True, user__is_superuser=False)
        return render(request, 'OBD_Campaigns/tareas_superuser.html', {
            'staff_profiles': staff_profiles
        })
    
# Vista detalles Staff 
@login_required
def detalle_staff(request, user_id):
    if not request.user.is_superuser:
        return render(request, '403.html')  # O redirigir como desees

    User = get_user_model()
    staff_user = get_object_or_404(User, id=user_id)
    profile = staff_user.profile
    comentario = Comentario.objects.filter(campania__vendedores=staff_user).distinct()
    campanas = Campana.objects.filter(vendedores=staff_user)
    tareas = Tarea.objects.filter(asignados=staff_user).distinct()

    return render(request, 'OBD_Campaigns/detalle_staff.html', {
        'staff_user': staff_user,
        'profile': profile,
        'campanas': campanas,
        'tareas': tareas,
        'comentarios': comentario
    })

# Vista para archivos live 
@login_required
def vista_archivos_live(request):
    query = request.GET.get('q', '')

    # Si es superusuario, ve todos los archivos
    if request.user.is_superuser:
        archivos = ArchivoLive.objects.all()

    else:
        # Vendedor (staff): campañas en las que está en vendedores
        campañas_staff = Campana.objects.filter(vendedores=request.user)
        # Cliente: campañas en las que es cliente
        campañas_cliente = Campana.objects.filter(cliente=request.user)

        # Unión de campañas asignadas
        campañas_asignadas = campañas_staff | campañas_cliente

        archivos = ArchivoLive.objects.filter(campana__in=campañas_asignadas)

    # Filtro de búsqueda
    if query:
        archivos = archivos.filter(
            Q(nombre_corto__icontains=query) |
            Q(campana__nombre_campana__icontains=query)
        )

    context = {
        'archivos': archivos,
        'query': query
    }
    return render(request, 'OBD_Campaigns/vista_archivos_live.html', context)