# app_Antiguedades/admin.py
from django.contrib import admin
from .models import Proveedor, Cliente, PiezaAntiguedad, ClienteProveedor

# Registrar todos los modelos
admin.site.register(Proveedor)
admin.site.register(Cliente)
admin.site.register(PiezaAntiguedad)
admin.site.register(ClienteProveedor)
