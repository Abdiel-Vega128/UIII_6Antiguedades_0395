# app_Antiguedades/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # General
    path('', views.inicio_antiguedades, name='inicio_antiguedades'),

    # CRUD Proveedores
    path('proveedores/', views.ver_proveedores, name='ver_proveedores'),
    path('proveedores/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/actualizar/<int:pk>/', views.actualizar_proveedor, name='actualizar_proveedor'),
    path('proveedores/actualizar/submit/<int:pk>/', views.realizar_actualizacion_proveedor, name='realizar_actualizacion_proveedor'),
    path('proveedores/borrar/<int:pk>/', views.borrar_proveedor, name='borrar_proveedor'),

    # CRUD Piezas de Antigüedad
    path('piezas/', views.ver_piezas, name='ver_piezas'),
    path('piezas/agregar/', views.agregar_pieza, name='agregar_pieza'),
    path('piezas/actualizar/<int:pk>/', views.actualizar_pieza, name='actualizar_pieza'),
    path('piezas/actualizar/submit/<int:pk>/', views.realizar_actualizacion_pieza, name='realizar_actualizacion_pieza'),
    path('piezas/borrar/<int:pk>/', views.borrar_pieza, name='borrar_pieza'),
    
    # CRUD Clientes (NUEVOS) 👥
    path('clientes/', views.ver_clientes, name='ver_clientes'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/actualizar/<int:pk>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/actualizar/submit/<int:pk>/', views.realizar_actualizacion_cliente, name='realizar_actualizacion_cliente'),
    path('clientes/borrar/<int:pk>/', views.borrar_cliente, name='borrar_cliente'),

    # CRUD Empleados
    path('empleados/', views.ver_empleados, name='ver_empleados'),
    path('empleados/agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('empleados/actualizar/<int:pk>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('empleados/borrar/<int:pk>/', views.borrar_empleado, name='borrar_empleado'),

    # CRUD Ventas
    path('ventas/', views.ver_ventas, name='ver_ventas'),
    path('ventas/agregar/', views.agregar_venta, name='agregar_venta'),
    path('ventas/actualizar/<int:pk>/', views.actualizar_venta, name='actualizar_venta'),
    path('ventas/borrar/<int:pk>/', views.borrar_venta, name='borrar_venta'),

    # CRUD Detalles de Venta
    path('detalleventas/', views.ver_detalleventas, name='ver_detalleventas'),
    path('detalleventas/agregar/', views.agregar_detalleventa, name='agregar_detalleventa'),
    path('detalleventas/actualizar/<int:pk>/', views.actualizar_detalleventa, name='actualizar_detalleventa'),
    path('detalleventas/borrar/<int:pk>/', views.borrar_detalleventa, name='borrar_detalleventa'),
]