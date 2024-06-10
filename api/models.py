from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, Permission
from .manager import CustomUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import timedelta

class Membresia(models.Model):
    """
    Modela una membresía en el sistema.

    Atributos:
        nombre (str): Nombre de la membresía.
        duracion (int): Duración de la membresía en meses.
        precio (Decimal): Precio de la membresía.
    """
    nombre = models.CharField(max_length=255, null=True)
    duracion = models.IntegerField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nombre
    
class Usuario(AbstractUser, PermissionsMixin):
    """
    Define un usuario en el sistema.

    Atributos:
        fecha_de_nacimiento (Date): Fecha de nacimiento del usuario.
        email (EmailField): Correo electrónico único del usuario.
        membresia (ForeignKey): Membresía asociada al usuario.
        fecha_inicio_membresia (Date): Fecha de inicio de la membresía.
    """
    membresia_choices = (
        (1, 'Membresia Básica'),
        (2, 'Membresia Plus'),
        (3, 'Membresia Premium'),
    )
    fecha_de_nacimiento = models.DateField(auto_now_add=False, blank=True, null=True)
    email = models.EmailField(unique=True, null=True)
    membresia = models.ForeignKey(Membresia, on_delete=models.CASCADE, null=False, default=1)
    fecha_inicio_membresia = models.DateField(default=timezone.now)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password', 'membresia']
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')

    def calcular_fecha_vencimiento(self):
        """
        Calcula la fecha de vencimiento de la membresía del usuario.

        Returns:
            Date: Fecha de vencimiento de la membresía.
        """
        return self.fecha_inicio_membresia + timedelta(days=self.membresia.duracion * 30)

    def obtener_cuenta_regresiva(self):
        """
        Obtiene la cuenta regresiva hasta la fecha de vencimiento de la membresía.

        Returns:
            timedelta: Diferencia de tiempo hasta la fecha de vencimiento.
        """
        fecha_vencimiento = self.calcular_fecha_vencimiento()
        diferencia = fecha_vencimiento - timezone.now().date()
        return diferencia

class Entrenador(models.Model):
    """
    Modela un entrenador en el sistema.

    Atributos:
        nombre (str): Nombre del entrenador.
        apellido (str): Apellido del entrenador.
        especialidad (str): Especialidad del entrenador.
        correo_electronico (EmailField): Correo electrónico del entrenador.
        numero_de_telefono (str): Número de teléfono del entrenador.
    """
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
    numero_de_telefono = models.CharField(max_length=15)

class EquipoDeportivo(models.Model):
    """
    Modela un equipo deportivo en el sistema.

    Atributos:
        nombre (str): Nombre del equipo deportivo.
        descripcion (str): Descripción del equipo deportivo.
        estado (str): Estado del equipo deportivo.
    """
    nombre_choices = (
        (1, 'Equipo de Boxeo'),
        (2, 'Equipo de Musculación'),
        (3, 'Equipo de Zumba'),
        (4, 'Equipo de Yoga'),
        (5, 'Equipo de Pilates'),
    )
    nombre = models.CharField(max_length=100, choices=nombre_choices, default=2, null=False)
    descripcion = models.TextField()
    estado = models.CharField(max_length=100)

class Clase(models.Model):
    """
    Modela una clase en el sistema.

    Atributos:
        nombre_clase (str): Nombre de la clase.
        descripcion (str): Descripción de la clase.
        entrenador (ForeignKey): Entrenador asociado a la clase.
        capacidad_maxima (int): Capacidad máxima de la clase.
        equipo (ForeignKey): Equipo deportivo asociado a la clase.
    """
    nombre_choices = (
        (1, 'Clase de Boxeo'),
        (2, 'Clase de Musculación'),
        (3, 'Clase de Zumba'),
        (4, 'Clase de Yoga'),
        (5, 'Clase de Pilates'),
    )
    nombre_clase = models.CharField(max_length=100, choices=nombre_choices, default=2, null=False)
    descripcion = models.TextField()
    entrenador = models.ForeignKey(Entrenador, on_delete=models.CASCADE, null=True, default=1)
    capacidad_maxima = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    equipo = models.ForeignKey(EquipoDeportivo, on_delete=models.CASCADE, null=True, default=1)

class ReservaClase(models.Model):
    """
    Modela una reserva de clase en el sistema.

    Atributos:
        clase (ForeignKey): Clase reservada.
        usuario (ForeignKey): Usuario que realiza la reserva.
        fecha (str): Fecha de la reserva.
        horario (str): Horario de la reserva.
    """
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, null=True, default=1)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, default=1)
    fecha = models.CharField(default=timezone.now)
    horario = models.CharField(default=timezone.now)
