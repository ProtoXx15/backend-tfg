from django.contrib import admin

from api.models import *


admin.site.register(Usuario)
admin.site.register(Membresía)
admin.site.register(Clase)
admin.site.register(EquipoDeportivo)
admin.site.register(Entrenador)
admin.site.register(ReservaClase)

# Register your models here.