from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .manager import CustomUserManager
from django.core.validators import MaxValueValidator, MinValueValidator

class Membresia(models.Model):
    tipo_de_membresia = models.CharField(max_length=100)
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.IntegerField()

    def str(self):
        return self.tipo_de_membresia
    
class Usuario(AbstractUser, PermissionsMixin):
    membresia_choices = (
    (1, 'Membresia Básica'),
    (2, 'Membresia Plus'),
    (3, 'Membresia Premium'),
)
    fecha_de_nacimiento = models.DateField(auto_now_add=False, blank=True, null=True)
    email = models.EmailField(unique=True,null=True)
    membresia = models.ForeignKey(Membresia, on_delete=models.CASCADE,null=False, default=3, choices=membresia_choices)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name','password','membresia']

class Entrenador(models.Model):
    especialidad_choices = (
        (1, 'Boxeo'),
        (2, 'Musculación'),
        (3, 'Zumba'),
        (4, 'Yoga'),
        (5, 'Pilates'),
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100, default=2, choices=especialidad_choices)
    correo_electronico = models.EmailField()
    número_de_teléfono = models.CharField(max_length=15)

    REQUIRED_FIELDS = ['nombre', 'apellido', 'especialidad', 'correo_electronico', 'numero_de_telefono']

class EquipoDeportivo(models.Model):
    nombre_choices = (
        (1, 'Equipo de Boxeo'),
        (2, 'Equipo de Musculación'),
        (3, 'Equipo de Zumba'),
        (4, 'Equipo de Yoga'),
        (5, 'Equipo de Pilates'),
    )
    nombre = models.CharField(max_length=100, choices=nombre_choices, default=2, null=False)
    descripción = models.TextField()
    estado = models.CharField(max_length=100)

class Clase(models.Model):
    nombre_choices = (
        (1, 'Clase de Boxeo'),
        (2, 'Clase de Musculación'),
        (3, 'Clase de Zumba'),
        (4, 'Clase de Yoga'),
        (5, 'Clase de Pilates'),
    )
    nombre_clase = models.CharField(max_length=100, choices=nombre_choices, default=2, null=False)
    descripción = models.TextField()
    entrenador = models.ForeignKey(Entrenador, on_delete=models.CASCADE, null=True, default=1)
    capacidad_máxima = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    horario = models.CharField(max_length=100)
    equipo = models.ForeignKey(EquipoDeportivo, on_delete=models.CASCADE, null=True, default=1)

    REQUIRED_FIELDS = ['nombre_clase', 'descripción', 'entrenador', 'capacidad_máxima', 'horario', 'equipo']


class ReservaClase(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, null=True, default=1)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, default=1)
    fecha = models.DateField(default=timezone.now)
    hora_de_entrada = models.TimeField()
    hora_de_salida = models.TimeField()
