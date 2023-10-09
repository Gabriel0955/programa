from django.contrib import admin
from .models import Categoria, Producto , dbProveedor , RolEmpleado

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(dbProveedor)
admin.site.register(RolEmpleado)
