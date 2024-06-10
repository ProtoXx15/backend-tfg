from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import *

Usuario = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'membresia')
        extra_kwargs = {'password': {'write_only': True}}


class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = '__all__'

class ReservaClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaClase
        fields = '__all__'

class ReservaClaseSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = ReservaClase
        fields = '__all__'
        depth = 2

class MembresiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membresia
        fields = ['id', 'nombre', 'duracion','precio']

class UsuarioDetailSerializer(serializers.ModelSerializer):
    membresia= MembresiaSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'membresia', 'fecha_inicio_membresia']

class EquipoDeportivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipoDeportivo
        fields = '__all__'

class EntrenadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrenador
        fields = '__all__'

class MiTokenObtenerParSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, usuario):
        token = super().get_token(usuario)

        # Agregar nombre del usuario al token
        token['nombre'] = usuario.nombre

        return token
    
class MiTokenObtenerParView(TokenObtainPairView):
    serializer_class = MiTokenObtenerParSerializer
