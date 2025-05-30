from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Campana(models.Model):
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    nombre_campana = models.CharField(max_length=255) 
    nombre_empresa = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='fotos_campanas/', blank=True, null=True)
    contacto_dueno = models.CharField(max_length=255)
    descripcion_campana = models.TextField(blank=True, null=True)
    fecha_creacion_campana = models.DateTimeField(auto_now_add=True)

    administrador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_superuser': True},
        related_name='campanas_admin'
    )
    vendedores = models.ManyToManyField(
        User,
        related_name='campanas_asignadas',
        limit_choices_to={'is_staff': True},
        blank=True
    )
    cliente = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='campanas_cliente'
    )

    def __str__(self):
        return f"{self.nombre_campana} - {self.nombre_empresa} (Admin: {self.administrador.username})"


class Item(models.Model):
    nombre_producto = models.CharField(max_length=255)
    desc_producto = models.TextField(blank=True, null=True)
    cantidad_disponible = models.PositiveIntegerField(default=0)
    cantidad_vendida = models.PositiveIntegerField(default=0)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to='fotos_items/', blank=True, null=True)
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"{self.nombre_producto} - {self.campana.nombre_campana}"


class ArchivoLive(models.Model):
    nombre_corto = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='archivos_lives/')
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, related_name='archivos_lives')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='archivos_subidos')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_corto} - {self.campana.nombre_campana}"
