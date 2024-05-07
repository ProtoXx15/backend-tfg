from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class UsuarioView(APIView):
    def get(self, request):
        usuario = Usuario.objects.all()
        serializer = UsuarioSerializer(usuario, many=True)
        return Response(serializer.data)
    
class ClaseView(APIView):
    def get(self, request):
        clase = Clase.objects.all()
        serializer = ClaseSerializer(clase, many=True)
        return Response(serializer.data)

class ReservaView(APIView):
    def get(self, request):
        reserva = Reserva.objects.all()
        serializer = ReservaSerializer(reserva, many=True)
        return Response(serializer.data)
    
class VentaView(APIView):
    def get(self, request):
        venta = Venta.objects.all()
        serializer = VentaSerializer(venta, many=True)
        return Response(serializer.data)
    
class InventarioView(APIView):
    def get(self, request):
        inventario = Inventario.objects.all()
        serializer = InventarioSerializer(inventario, many=True)
        return Response(serializer.data)
    
class proveedorView(APIView):
    def get(self, request):
        proveedor = proveedor.objects.all()
        serializer = proveedorSerializer(proveedor, many=True)
        return Response(serializer.data)
    
class ProductoView(APIView):
    def get(self, request):
        producto = Producto.objects.all()
        serializer = ProductoSerializer(producto, many=True)
        return Response(serializer.data)
