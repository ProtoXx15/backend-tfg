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

class ReservaSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True, many=False)
    clase = ClaseSerializer(read_only=True, many=False)
    class Meta:
        model = Reserva
        fields = '__all__'

class proveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    proveedor = proveedorSerializer(read_only=True, many=False)
    class Meta:
        model = Producto
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True, many=False)
    producto = ProductoSerializer(read_only=True, many=False)
    class Meta:
        model = Venta
        fields = '__all__'

class InventarioSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True, many=False)
    proveedor = proveedorSerializer(read_only=True, many=False)
    class Meta:
        model = Inventario
        fields = '__all__'




