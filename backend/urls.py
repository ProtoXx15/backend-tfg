from django.contrib import admin
from django.urls import path, include
from api.views import *

urlpatterns = [
    # Rutas para las operaciones de autenticación
    path('api/login/', login),
    path('api/logout/', logout),
    path('api/register/', register),
    path('api/delete/', delete_user),

    # Ruta para ver los detalles de un usuario
    path('api/detalles_usuario/', UsuarioDetailView.as_view(), name='user-detail'),

    # Ruta para crear un usuario
    path('register/', UsuarioCreate.as_view(), name='user-create'),

    # Ruta para obtener un token de autenticación
    path('token/', MiTokenObtenerParView.as_view(), name='token_obtain_pair'),

    # Ruta para acceder al panel de administración de Django
    path('admin/', admin.site.urls),

    # Rutas para las operaciones de los usuarios
    path('api/usuario/', UsuarioListCreateView.as_view()),
    path('api/usuario/<int:pk>/', UsuarioRetrieveUpdateView.as_view()),

    # Rutas para las operaciones de las clases
    path('api/clase/', ClaseListCreateView.as_view()),
    path('api/clase/<int:pk>/', ClaseRetrieveUpdateView.as_view()),

    # Rutas para las operaciones de las membresías
    path('api/membresia/<int:pk>/', MembresiaRetrieveUpdateView.as_view()),
    path('api/membresia/', MembresiaListCreateView.as_view()),

    # Rutas para las operaciones de los equipos deportivos
    path('api/equipodeportivo/', EquipoDeportivoListCreateView.as_view()),
    path('api/equipodeportivo/<int:pk>/', EquipoDeportivoRetrieveUpdateView.as_view()),

    # Rutas para las operaciones de los entrenadores
    path('api/entrenador/', EntrenadorListCreateView.as_view()),
    path('api/entrenador/<int:pk>/', EntrenadorRetrieveUpdateView.as_view()),

    # Ruta para reservar una clase
    path('api/reservar_clase/', ReservarClaseAPIView.as_view(), name='reservar_clase'),

    # Ruta para cancelar una reserva de clase
    path('api/cancelar_reserva/<str:fecha>/<str:horario>/<str:clase>/', cancelar_reserva, name='cancelar_reserva'),

    # Ruta para verificar una reserva
    path('api/verificar_reserva/', VerificarReservaAPIView.as_view(), name='verificar_reserva'),
]


