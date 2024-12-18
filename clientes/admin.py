from django.contrib import admin
from .models import Cliente, Modelo, Auto, Pedido, DetalleCompra

admin.site.register(Cliente)
admin.site.register(Modelo)
admin.site.register(Auto)
admin.site.register(Pedido)
admin.site.register(DetalleCompra)