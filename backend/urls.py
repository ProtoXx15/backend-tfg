from django.contrib import admin
from django.urls import path
from api.views import MiTokenObtenerParView
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import *

urlpatterns = [
    path('api/login/', login),
    path('api/logout/', logout),
    path('api/register/', register),
    path('api/delete/', delete_user),
    path('admin/', admin.site.urls),
    path('api/usuario/', UsuarioListCreateView.as_view()),
    path('api/usuario/<int:pk>/', UsuarioRetrieveUpdateView.as_view()),
    path('api/clase/', ClaseListCreateView.as_view()),
    path('api/clase/<int:pk>/', ClaseRetrieveUpdateView.as_view()),
    path('api/membresia/<int:pk>/', MembresiaRetrieveUpdateView.as_view()),
    path('api/membresia/', MembresiaListCreateView.as_view()),
    path('api/equipodeportivo/', EquipoDeportivoListCreateView.as_view()),
    path('api/equipodeportivo/<int:pk>/', EquipoDeportivoRetrieveUpdateView.as_view()),
    path('api/entrenador/', EntrenadorListCreateView.as_view()),
    path('api/entrenador/<int:pk>/', EntrenadorRetrieveUpdateView.as_view()),
    path('api/reservar_clase/', ReservarClaseAPIView.as_view(), name='reservar_clase'),
    path('api/cancelar_reserva/<str:fecha>/<str:horario>/<str:clase>/', cancelar_reserva, name='cancelar_reserva'),
    path('api/verificar_reserva/', VerificarReservaAPIView.as_view(), name='verificar_reserva'),
    path('api/detalles_usuario/', detalles_usuario),
]

