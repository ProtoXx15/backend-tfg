from django.contrib.auth.models import BaseUserManager

# Definición de la clase del gestor de usuarios personalizado
class CustomUserManager(BaseUserManager):

    # Método para crear un usuario normal
    def create_user(self, username, first_name, last_name, email, password, membresia, **extra_fields):
        # Verificar si se da un correo electrónico
        if not email:
            raise ValueError('Debes introducir un email')
        
        # Normalizar el correo electrónico
        email = self.normalize_email(email)

        # Importar el modelo de membresía
        from .models import Membresia
        # Obtener el objeto de membresía correspondiente al id proporcionado
        membresiaobj = Membresia.objects.get(pk=membresia)

        # Crear un nuevo usuario con los datos proporcionados y el objeto de membresía asociado
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            membresia=membresiaobj,  
            **extra_fields
        )
        # Establecer la contraseña utilizando el método proporcionado por Django
        user.set_password(password)
        # Guardar el usuario en la base de datos
        user.save(using=self._db)
        # Devolver el usuario creado
        return user

    # Método para crear un superusuario
    def create_superuser(self, username, first_name, last_name, email, password, membresia, **extra_fields):
        # Establecer algunos campos adicionales por defecto para el superusuario
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Verificar que el superusuario tenga los atributos adecuados establecidos
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super usuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super usuario debe tener is_superuser=True.')
        
        # Llamar al método create_user para crear el superusuario
        return self.create_user(username, first_name, last_name, email, password, membresia, **extra_fields)
