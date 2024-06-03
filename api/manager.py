from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Administrador de usuarios personalizado para este proyecto.
    """
    def create_user(self, username, first_name, last_name, email, password, membresia, **extra_fields):
        """
        Crear y guardar un usuario con el email y password proporcionado.
        """
        if not email:
            raise ValueError('Debes introducir un email')
        email = self.normalize_email(email)

        # Importar Membresia aquí para evitar la importación circular
        from .models import Membresia
        membresiaobj = Membresia.objects.get(pk=membresia)

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            membresia=membresiaobj,  # Pasar la instancia de Membresia en lugar del ID
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password, membresia, **extra_fields):
        """
        Crear y guardar un superusuario con el email y password proporcionado.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super usuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super usuario debe tener is_superuser=True.')
        
        return self.create_user(username, first_name, last_name, email, password, membresia, **extra_fields)
