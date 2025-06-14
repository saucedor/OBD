from django.urls import path
from . import views

urlpatterns = [
    path('campanas/', views.vista_campanas, name='vista_campanas'),
    path('campanas/<int:pk>/detalle/', views.detalle_campana, name='detalle_campana'),
    path('campanas/<int:pk>/borrar_confirmacion/', views.borrar_confirmacion_campana, name='borrar_confirmacion_campana'),
    path('campanas/<int:pk>/borrar/', views.borrar_campana, name='borrar_campana'),
    path('campanas/nueva/', views.crear_campana, name='crear_campana'),
    path('campanas/<int:pk>/detalle/', views.detalle_campana, name='detalle_campana'),
    path('campanas/<int:campana_id>/items/', views.items_campana_view, name='items_campana'),
    path('campanas/<int:campana_id>/inventario/nuevo/', views.crear_item, name='crear_item'),
    path('campanas/<int:campana_id>/archivos-live/', views.archivolive_campana, name='archivolive_campana'),
    path('campanas/<int:campana_id>/archivos-live/crear/', views.crear_archivolive, name='crear_archivolive'),
    path('campanas/<int:pk>/cargar_items_csv/', views.importar_items_csv, name='importar_items_csv'),
    path('items/<int:item_id>/editar/', views.editar_item, name='editar_item'),
    path('archivos/<int:archivo_id>/editar/', views.editar_archivo_live, name='editar_archivo_live'),
    path('archivos/<int:archivo_id>/eliminar/', views.eliminar_archivo_live, name='eliminar_archivo'),
    path('items/<int:item_id>/eliminar/', views.eliminar_item, name='eliminar_item'),
    path('campanas/<int:campania_id>/comentarios/subir/', views.subir_csv_comentarios, name='subir_csv_comentarios'),
    path('campanas/<int:campania_id>/comentarios/', views.comentarios_por_campana, name='comentarios_campana'),
    path('campanas/<int:campania_id>/comentarios/procesar/', views.procesar_comentarios, name='procesar_comentarios'),
    path('campanas/<int:campania_id>/comentarios/asignar/', views.asignar_tareas, name='asignar_tareas'),
    path('comentarios/', views.lista_comentarios, name='lista_comentarios'),
    path('tareas/staff/', views.vista_tareas_staff, name='tareas_staff'),
    path('tareas/superuser/', views.vista_tareas_superuser, name='tareas_superuser'),
    path('tareas/staff/<int:user_id>/', views.detalle_staff, name='detalle_staff'),
    path('archivos/', views.vista_archivos_live, name='vista_archivos_live'),
]

