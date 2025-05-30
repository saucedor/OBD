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
]

