from django.contrib import admin

from api.models import *


admin.site.register(Usuario)
admin.site.register(Clase)
admin.site.register(Reserva)
admin.site.register(Venta)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Inventario)

# Register your models here.