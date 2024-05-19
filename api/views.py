from api.models import *
from api.serializers import *
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Membresia
from django.urls import reverse_lazy

@api_view(['POST'])
def register(request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = Usuario.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(Usuario, username=request.data.get('username'))
    if not user.check_password(request.data.get('password')):
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UsuarioSerializer(instance=user)
    return Response({'token': token.key,'user': serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def logout(request):
    token = request.auth
    token.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_user(request):
    user = request.user
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



# Usuario
class UsuarioListCreateView(generics.ListCreateAPIView):
    serializer_class = UsuarioSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Usuario.objects.all()
        else:
            return [self.request.user]

class UsuarioRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UsuarioSerializer
    permission_classes= [IsAuthenticated]
    def update(self, request, *args, **kwargs):
        # Hashear la contraseña si está presente en los datos de la solicitud
        user = self.get_object()
        if 'password' in request.data:
            user.set_password(request.data['password'])
            user.save()
            request.data.pop('password')  # Eliminar la contraseña del diccionario de datos

        return super().update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Hashear la contraseña si está presente en los datos de la solicitud
        if 'password' in request.data:
            request.data['password'] = make_password(request.data['password'])
        return self.partial_update(request, *args, **kwargs)
    def get_object(self):
        return self.request.user
    def delete(self, request, *args, **kwargs):
        token = self.request.auth
        token.delete()
        return super().delete(request, *args, **kwargs)
    

#Membresía   
class MembresiaListCreateView(generics.ListCreateAPIView):
   permission_classes= [IsAuthenticated]
   serializer_class = MembresiaSerializer
   def get_queryset(self):
        if self.request.user.is_superuser:
            return Membresia.objects.all()

class MembresiaRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = MembresiaSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Membresia.objects.all()

# ReservaClase
class ReservaClaseListCreateView(generics.ListCreateAPIView):
    serializer_class = ReservaClaseSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return ReservaClase.objects.all()
        else:
            return ReservaClase.objects.filter(usuario=self.request.user)

class ReservaClaseRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ReservaClaseSerializer
    permission_classes= [IsAuthenticated]

# Clase
class ClaseListCreateView(generics.ListCreateAPIView):
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer

class ClaseRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer

# Entrenador
class EntrenadorListCreateView(generics.ListCreateAPIView):
    serializer_class = EntrenadorSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Entrenador.objects.all()

class EntrenadorRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = EntrenadorSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Entrenador.objects.all()

# EquipoDeportivo
class EquipoDeportivoListCreateView(generics.ListCreateAPIView):
    serializer_class = EquipoDeportivoSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return EquipoDeportivo.objects.all()

class EquipoDeportivoRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = EquipoDeportivoSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return EquipoDeportivo.objects.all()


