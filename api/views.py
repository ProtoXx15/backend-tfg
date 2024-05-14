from api.models import *
from api.serializers import *
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

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

# Usuario
class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# Clase
class ClaseListCreateView(generics.ListCreateAPIView):
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer

class ClaseRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer

#Membresía
class MembresiaListCreateView(generics.ListCreateAPIView):
    queryset = Membresía.objects.all()
    serializer_class = MembresíaSerializer

class MembresiaRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Membresía.objects.all()
    serializer_class = MembresíaSerializer

# EquipoDeportivo
class EquipoDeportivoListCreateView(generics.ListCreateAPIView):
    queryset = EquipoDeportivo.objects.all()
    serializer_class = EquipoDeportivoSerializer

class EquipoDeportivoRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = EquipoDeportivo.objects.all()
    serializer_class = EquipoDeportivoSerializer

# Entrenador
class EntrenadorListCreateView(generics.ListCreateAPIView):
    queryset = Entrenador.objects.all()
    serializer_class = EntrenadorSerializer

class EntrenadorRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Entrenador.objects.all()
    serializer_class = EntrenadorSerializer

# ReservaClase
class ReservaClaseListCreateView(generics.ListCreateAPIView):
    queryset = ReservaClase.objects.all()
    serializer_class = ReservaClaseSerializer

class ReservaClaseRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ReservaClase.objects.all()
    serializer_class = ReservaClaseSerializer
