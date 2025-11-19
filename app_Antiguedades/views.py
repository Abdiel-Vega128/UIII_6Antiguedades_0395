# app_Antiguedades/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor, PiezaAntiguedad, Cliente, Empleado, Venta, DetalleVenta
from django.http import HttpResponse

# ==========================================
# GENERAL
# ==========================================
def inicio_antiguedades(request):
    """Página de inicio."""
    return render(request, 'inicio.html')

# ==========================================
# VISTAS CRUD PROVEEDOR (Existentes)
# ==========================================
def agregar_proveedor(request):
    if request.method == 'POST':
        Proveedor.objects.create(
            nombre_empresa=request.POST.get('nombre_empresa'),
            contacto=request.POST.get('contacto'),
            email=request.POST.get('email'),
            telefono=request.POST.get('telefono'),
            direccion=request.POST.get('direccion'),
            especialidad=request.POST.get('especialidad'),
            años_experiencia=request.POST.get('años_experiencia')
        )
        return redirect('ver_proveedores')
    return render(request, 'proveedor/agregar_proveedor.html')

def ver_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedor/ver_proveedores.html', {'proveedores': proveedores})

def actualizar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    return render(request, 'proveedor/actualizar_proveedor.html', {'proveedor': proveedor})

def realizar_actualizacion_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.nombre_empresa = request.POST.get('nombre_empresa')
        proveedor.contacto = request.POST.get('contacto')
        proveedor.email = request.POST.get('email')
        proveedor.telefono = request.POST.get('telefono')
        proveedor.direccion = request.POST.get('direccion')
        proveedor.especialidad = request.POST.get('especialidad')
        proveedor.años_experiencia = request.POST.get('años_experiencia')
        proveedor.save()
        return redirect('ver_proveedores')
    return redirect('actualizar_proveedor', pk=pk) 

def borrar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('ver_proveedores')
    return render(request, 'proveedor/borrar_proveedor.html', {'proveedor': proveedor})

# ==========================================
# VISTAS CRUD PIEZA DE ANTIGÜEDAD (Existentes)
# ==========================================
def agregar_pieza(request):
    proveedores = Proveedor.objects.all()
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        proveedor_obj = get_object_or_404(Proveedor, pk=request.POST.get('proveedor'))
        comprador_id = request.POST.get('comprador')
        comprador_obj = get_object_or_404(Cliente, pk=comprador_id) if comprador_id else None
        fecha_venta = request.POST.get('fecha_venta') if request.POST.get('fecha_venta') else None
        precio_venta = request.POST.get('precio_venta') if request.POST.get('precio_venta') else None
        PiezaAntiguedad.objects.create(
            nombre=request.POST.get('nombre'),
            descripcion=request.POST.get('descripcion'),
            precio=request.POST.get('precio'),
            año_fabricacion=request.POST.get('año_fabricacion'),
            estado_conservacion=request.POST.get('estado_conservacion'),
            proveedor=proveedor_obj,
            comprador=comprador_obj,
            fecha_venta=fecha_venta,
            precio_venta=precio_venta,
            imagen=request.FILES.get('imagen')
        )
        return redirect('ver_piezas')
    return render(request, 'pieza/agregar_pieza.html', {'proveedores': proveedores, 'clientes': clientes})

def ver_piezas(request):
    piezas = PiezaAntiguedad.objects.all()
    return render(request, 'pieza/ver_piezas.html', {'piezas': piezas})

def actualizar_pieza(request, pk):
    pieza = get_object_or_404(PiezaAntiguedad, pk=pk)
    proveedores = Proveedor.objects.all()
    clientes = Cliente.objects.all()
    return render(request, 'pieza/actualizar_pieza.html', {'pieza': pieza, 'proveedores': proveedores, 'clientes': clientes})

def realizar_actualizacion_pieza(request, pk):
    pieza = get_object_or_404(PiezaAntiguedad, pk=pk)
    if request.method == 'POST':
        pieza.nombre = request.POST.get('nombre')
        pieza.descripcion = request.POST.get('descripcion')
        pieza.precio = request.POST.get('precio')
        pieza.año_fabricacion = request.POST.get('año_fabricacion')
        pieza.estado_conservacion = request.POST.get('estado_conservacion')
        proveedor_id = request.POST.get('proveedor')
        pieza.proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
        comprador_id = request.POST.get('comprador')
        pieza.comprador = get_object_or_404(Cliente, pk=comprador_id) if comprador_id else None
        pieza.fecha_venta = request.POST.get('fecha_venta') if request.POST.get('fecha_venta') else None
        pieza.precio_venta = request.POST.get('precio_venta') if request.POST.get('precio_venta') else None
        if 'imagen' in request.FILES:
            pieza.imagen = request.FILES['imagen']
        pieza.save()
        return redirect('ver_piezas')
    return redirect('actualizar_pieza', pk=pk)

def borrar_pieza(request, pk):
    pieza = get_object_or_404(PiezaAntiguedad, pk=pk)
    if request.method == 'POST':
        pieza.delete()
        return redirect('ver_piezas')
    return render(request, 'pieza/borrar_pieza.html', {'pieza': pieza})

# ==========================================
# VISTAS CRUD CLIENTE (NUEVAS) 👥
# ==========================================

def agregar_cliente(request):
    """Muestra el formulario y maneja la adición de un nuevo cliente."""
    piezas = PiezaAntiguedad.objects.all()
    if request.method == 'POST':
        es_coleccionista = request.POST.get('es_coleccionista') == 'on' # Maneja el checkbox

        cliente = Cliente.objects.create(
            nombre=request.POST.get('nombre'),
            email=request.POST.get('email'),
            telefono=request.POST.get('telefono'),
            direccion=request.POST.get('direccion'),
            estado_civil=request.POST.get('estado_civil'),
            es_coleccionista=es_coleccionista
        )
        piezas_ids = [int(id) for id in request.POST.getlist('piezas_compradas') if id]
        piezas = PiezaAntiguedad.objects.filter(id__in=piezas_ids)
        cliente.piezas_compradas.set(piezas)
        return redirect('ver_clientes')

    return render(request, 'cliente/agregar_cliente.html', {'piezas': piezas})

def ver_clientes(request):
    """Muestra la lista de todos los clientes."""
    clientes = Cliente.objects.all()
    return render(request, 'cliente/ver_clientes.html', {'clientes': clientes})

def actualizar_cliente(request, pk):
    """Muestra el formulario para actualizar un cliente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    piezas = PiezaAntiguedad.objects.all()
    return render(request, 'cliente/actualizar_cliente.html', {'cliente': cliente, 'piezas': piezas})

def realizar_actualizacion_cliente(request, pk):
    """Procesa la actualización de un cliente."""
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        es_coleccionista = request.POST.get('es_coleccionista') == 'on' # Maneja el checkbox

        cliente.nombre = request.POST.get('nombre')
        cliente.email = request.POST.get('email')
        cliente.telefono = request.POST.get('telefono')
        cliente.direccion = request.POST.get('direccion')
        cliente.estado_civil = request.POST.get('estado_civil')
        cliente.es_coleccionista = es_coleccionista

        cliente.save()
        piezas_ids = [int(id) for id in request.POST.getlist('piezas_compradas') if id]
        piezas = PiezaAntiguedad.objects.filter(id__in=piezas_ids)
        cliente.piezas_compradas.set(piezas)
        return redirect('ver_clientes')

    return redirect('actualizar_cliente', pk=pk)

def borrar_cliente(request, pk):
    """Muestra la confirmación para borrar un cliente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_clientes')

    return render(request, 'cliente/borrar_cliente.html', {'cliente': cliente})

# ==========================================
# VISTAS CRUD EMPLEADO
# ==========================================
def agregar_empleado(request):
    if request.method == 'POST':
        Empleado.objects.create(
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            puesto=request.POST.get('puesto'),
            salario=request.POST.get('salario'),
            telefono=request.POST.get('telefono')
        )
        return redirect('ver_empleados')
    return render(request, 'empleado/agregar_empleado.html')

def ver_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleado/ver_empleados.html', {'empleados': empleados})

def actualizar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre')
        empleado.apellido = request.POST.get('apellido')
        empleado.puesto = request.POST.get('puesto')
        empleado.salario = request.POST.get('salario')
        empleado.telefono = request.POST.get('telefono')
        empleado.save()
        return redirect('ver_empleados')
    return render(request, 'empleado/actualizar_empleado.html', {'empleado': empleado})

def borrar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('ver_empleados')
    return render(request, 'empleado/borrar_empleado.html', {'empleado': empleado})

# ==========================================
# VISTAS CRUD VENTA
# ==========================================
def agregar_venta(request):
    empleados = Empleado.objects.all()
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        empleado_obj = get_object_or_404(Empleado, pk=request.POST.get('empleado'))
        cliente_obj = get_object_or_404(Cliente, pk=request.POST.get('cliente'))
        Venta.objects.create(
            fecha_venta=request.POST.get('fecha_venta'),
            total=request.POST.get('total'),
            metodo_pago=request.POST.get('metodo_pago'),
            empleado=empleado_obj,
            cliente=cliente_obj
        )
        return redirect('ver_ventas')
    return render(request, 'venta/agregar_venta.html', {'empleados': empleados, 'clientes': clientes})

def ver_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'venta/ver_ventas.html', {'ventas': ventas})

def actualizar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    empleados = Empleado.objects.all()
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        venta.fecha_venta = request.POST.get('fecha_venta')
        venta.total = request.POST.get('total')
        venta.metodo_pago = request.POST.get('metodo_pago')
        empleado_id = request.POST.get('empleado')
        venta.empleado = get_object_or_404(Empleado, pk=empleado_id)
        cliente_id = request.POST.get('cliente')
        venta.cliente = get_object_or_404(Cliente, pk=cliente_id)
        venta.save()
        return redirect('ver_ventas')
    return render(request, 'venta/actualizar_venta.html', {'venta': venta, 'empleados': empleados, 'clientes': clientes})

def borrar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('ver_ventas')
    return render(request, 'venta/borrar_venta.html', {'venta': venta})

# ==========================================
# VISTAS CRUD DETALLE VENTA
# ==========================================
def agregar_detalleventa(request):
    ventas = Venta.objects.all()
    piezas = PiezaAntiguedad.objects.all()
    if request.method == 'POST':
        venta_obj = get_object_or_404(Venta, pk=request.POST.get('venta'))
        pieza_obj = get_object_or_404(PiezaAntiguedad, pk=request.POST.get('pieza_antiguedad'))
        DetalleVenta.objects.create(
            venta=venta_obj,
            pieza_antiguedad=pieza_obj,
            cantidad=request.POST.get('cantidad'),
            precio_unitario=request.POST.get('precio_unitario'),
            subtotal=request.POST.get('subtotal'),
            total=request.POST.get('total')
        )
        return redirect('ver_detalleventas')
    return render(request, 'detalleventa/agregar_detalleventa.html', {'ventas': ventas, 'piezas': piezas})

def ver_detalleventas(request):
    detalleventas = DetalleVenta.objects.all()
    return render(request, 'detalleventa/ver_detalleventas.html', {'detalleventas': detalleventas})

def actualizar_detalleventa(request, pk):
    detalleventa = get_object_or_404(DetalleVenta, pk=pk)
    ventas = Venta.objects.all()
    piezas = PiezaAntiguedad.objects.all()
    if request.method == 'POST':
        detalleventa.venta = get_object_or_404(Venta, pk=request.POST.get('venta'))
        detalleventa.pieza_antiguedad = get_object_or_404(PiezaAntiguedad, pk=request.POST.get('pieza_antiguedad'))
        detalleventa.cantidad = request.POST.get('cantidad')
        detalleventa.precio_unitario = request.POST.get('precio_unitario')
        detalleventa.subtotal = request.POST.get('subtotal')
        detalleventa.total = request.POST.get('total')
        detalleventa.save()
        return redirect('ver_detalleventas')
    return render(request, 'detalleventa/actualizar_detalleventa.html', {'detalleventa': detalleventa, 'ventas': ventas, 'piezas': piezas})

def borrar_detalleventa(request, pk):
    detalleventa = get_object_or_404(DetalleVenta, pk=pk)
    if request.method == 'POST':
        detalleventa.delete()
        return redirect('ver_detalleventas')
    return render(request, 'detalleventa/borrar_detalleventa.html', {'detalleventa': detalleventa})
