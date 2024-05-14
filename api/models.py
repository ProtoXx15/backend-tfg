from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager

class Usuario(AbstractUser ):
    fecha_de_nacimiento = models.DateField(auto_now_add=False, blank=True, null=True)
    email = models.EmailField(unique=True,null=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','password']

class Membresía(models.Model):
    tipo_de_membresía = models.CharField(max_length=100)
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    duración = models.IntegerField()

class Entrenador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    número_de_teléfono = models.CharField(max_length=15)

class EquipoDeportivo(models.Model):
    nombre = models.CharField(max_length=100)
    descripción = models.TextField()
    disponibilidad = models.IntegerField()
    estado = models.CharField(max_length=100)

class Clase(models.Model):
    nombre = models.CharField(max_length=100)
    descripción = models.TextField()
    entrenador = models.ForeignKey(Entrenador, on_delete=models.CASCADE, null=True, default=1)
    capacidad_máxima = models.IntegerField()
    horario = models.CharField(max_length=100)
    equipo = models.ForeignKey(EquipoDeportivo, on_delete=models.CASCADE, null=True, default=1)


class ReservaClase(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, null=True, default=1)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, default=1)
    fecha = models.DateField(default=timezone.now)
    hora_de_entrada = models.TimeField()
    hora_de_salida = models.TimeField()
