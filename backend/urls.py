from django.contrib import admin
from django.urls import path
from api.views import *


urlpatterns = [
    path('api/login/', login),
    path('api/logout/', logout),
    path('api/register/', register),
    path('admin/', admin.site.urls),
    path('api/usuario/', UsuarioListCreateView.as_view()),
    path('api/usuario/<int:pk>/', UsuarioRetrieveUpdateView.as_view()),
    path('api/clase/', ClaseListCreateView.as_view()),
    path('api/clase/<int:pk>/', ClaseRetrieveUpdateView.as_view()),
    path('api/membresia/', MembresiaListCreateView.as_view()),
    path('api/membresia/<int:pk>/', MembresiaRetrieveUpdateView.as_view()),
    path('api/equipodeportivo/', EquipoDeportivoListCreateView.as_view()),
    path('api/equipodeportivo/<int:pk>/', EquipoDeportivoRetrieveUpdateView.as_view()),
    path('api/entrenador/', EntrenadorListCreateView.as_view()),
    path('api/entrenador/<int:pk>/', EntrenadorRetrieveUpdateView.as_view()),
    path('api/reservaclase/', ReservaClaseListCreateView.as_view()),
    path('api/reservaclase/<int:pk>/', ReservaClaseRetrieveUpdateView.as_view()),
]

