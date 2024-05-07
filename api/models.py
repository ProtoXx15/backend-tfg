from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    rol = models.CharField(max_length=100)

    # Add related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",  # Changed related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",  # Changed related_name
        related_query_name="user",
    )

class Clase(models.Model):
    nombre_clase = models.CharField(max_length=255)
    descripcion = models.TextField()
    horario = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255)
    cupo_maximo = models.IntegerField()

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField()

class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=255)
    contacto = models.CharField(max_length=255)
    correo_electronico = models.EmailField()
    telefono = models.CharField(max_length=100)

class Producto(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    nombre_producto = models.CharField(max_length=255)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

class Venta(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField()
    cantidad = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
