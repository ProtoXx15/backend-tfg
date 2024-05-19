from rest_framework import serializers
from api.models import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = '__all__'

class ReservaClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaClase
        fields = '__all__'

class MembresiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membresia
        fields = ['id', 'tipo_de_membresía', 'precio_mensual', 'duración']

class EquipoDeportivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipoDeportivo
        fields = '__all__'

class EntrenadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrenador
        fields = '__all__'
