from django.contrib import admin
from .models import Campana, Item, ArchivoLive, Comentario, Tarea

# Register your models here.
admin.site.register(ArchivoLive)
admin.site.register(Comentario) 
admin.site.register(Campana)
admin.site.register(Item)
admin.site.register(Tarea)