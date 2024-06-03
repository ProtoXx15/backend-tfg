from api.models import *
from api.serializers import *
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import *
from .models import Membresia
from .serializers import UsuarioSerializer
import logging
from django.contrib.auth.models import update_last_login
from django.http import JsonResponse
from django.contrib.auth.models import User
from api.models import ReservaClase, Clase
from api.serializers import UsuarioSerializer, ReservaClaseSerializer, ClaseSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)

@api_view(['POST'])
def register(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    # Obtener el usuario por el nombre de usuario
    user = get_object_or_404(Usuario, username=request.data['username'])

    # Verificar las credenciales del usuario
    if not user.check_password(request.data['password']):
        return Response({'details': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)

    # Actualizar la fecha de último inicio de sesión
    update_last_login(None, user)

    # Generar o obtener el token de autenticación
    token, created = Token.objects.get_or_create(user=user)

    # Serializar el usuario para incluirlo en la respuesta
    serializer = UsuarioSerializer(instance=user)

    if user.is_superuser:
        return Response({'token': token.key, 'user': serializer.data, 'is_superuser': True}, status=status.HTTP_200_OK)
    else:
        return Response({'token': token.key, 'user': serializer.data, 'is_superuser': False}, status=status.HTTP_200_OK)


   
@api_view(['GET'])
def logout(request):
    try: 
        token = request.auth
        token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request):
    user = request.user
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def detalles_usuario(request):
    user=request.user
    serializer = UsuarioSerializer(user)
    return Response(serializer.data, status=200)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def listar_todos_usuarios(request):
#     if not request.user.is_superuser:
#         return Response({'detail': 'No tienes permiso para ver esta información.'}, status=status.HTTP_403_FORBIDDEN)
    
#     usuarios = User.objects.all()
#     serializer = UsuarioSerializer(usuarios, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)



# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def eliminar_cualquier_usuario(request, usuario_id):
#     if not request.user.is_superuser:
#         return Response({'detail': 'No tienes permiso para eliminar este usuario.'}, status=status.HTTP_403_FORBIDDEN)
    
#     usuario = get_object_or_404(User, id=usuario_id)
#     usuario.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def eliminar_cualquier_clase(request, clase_id):
#     if not request.user.is_superuser:
#         return Response({'detail': 'No tienes permiso para eliminar esta clase.'}, status=status.HTTP_403_FORBIDDEN)
    
#     clase = get_object_or_404(Clase, id=clase_id)
#     clase.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)

# Usuario
class UsuarioListCreateView(generics.ListCreateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Usuario.objects.all()
        return Usuario.objects.filter(id=self.request.user.id)

class UsuarioRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        # Verifica si el usuario actual es el mismo que el usuario que se va a editar
        if user == request.user or request.user.is_superuser:
            if 'password' in request.data:
                user.set_password(request.data['password'])
                user.save()
                request.data.pop('password')
            return super().update(request, *args, **kwargs)
        else:
            return Response({'detail': 'No tienes permiso para editar este usuario.'}, status=403)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()

        # Verifica si el usuario actual es el mismo que el usuario que se va a borrar
        if user == request.user or request.user.is_superuser:
            token = self.request.auth
            if token:
                token.delete()
            return super().delete(request, *args, **kwargs)
        else:
            return Response({'detail': 'No tienes permiso para borrar este usuario.'}, status=403)

    
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
class VerificarReservaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        reservations = ReservaClase.objects.filter(usuario=user)
        serializer = ReservaClaseSerializerAll(reservations, many=True)
        return Response({"reservations": serializer.data}, status=status.HTTP_200_OK)

class ReservarClaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = ReservaClaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def cancelar_reserva(request, fecha, horario, clase):
    user = request.user
    reserva = ReservaClase.objects.filter(usuario=user, fecha=fecha, horario=horario, clase=clase)
    if reserva.exists():
        reserva.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


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