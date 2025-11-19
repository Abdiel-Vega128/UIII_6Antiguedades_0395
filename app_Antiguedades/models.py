# app_Antiguedades/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# ==========================================
# MODELO: PROVEEDOR
# ==========================================
class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=200, verbose_name="Nombre de la empresa")
    contacto = models.CharField(max_length=100, verbose_name="Persona de contacto")
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono", blank=True, null=True)
    direccion = models.TextField(verbose_name="Dirección")
    especialidad = models.CharField(max_length=100, verbose_name="Especialidad")
    años_experiencia = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Años de experiencia"
    )
    
    def __str__(self):
        return f"{self.nombre_empresa} - {self.contacto}"
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre_empresa']

# ==========================================
# MODELO: CLIENTE
# ==========================================
class Cliente(models.Model):
    ESTADOS_CIVILES = [
        ('S', 'Soltero/a'),
        ('C', 'Casado/a'),
        ('V', 'Viudo/a'),
        ('D', 'Divorciado/a'),
    ]
    
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono", blank=True, null=True)
    direccion = models.TextField(verbose_name="Dirección")
    fecha_registro = models.DateField(auto_now_add=True, verbose_name="Fecha de registro")
    estado_civil = models.CharField(max_length=1, choices=ESTADOS_CIVILES, verbose_name="Estado civil")
    es_coleccionista = models.BooleanField(default=False, verbose_name="Es coleccionista")
    
    # RELACIÓN M:M con Proveedor
    proveedores_favoritos = models.ManyToManyField(
        Proveedor,
        through='ClienteProveedor',
        related_name='clientes',
        verbose_name="Proveedores favoritos",
        blank=True
    )
    
    def __str__(self):
        return f"{self.nombre} ({self.email})"
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre']

# ==========================================
# MODELO: PIEZA DE ANTIGÜEDAD (ACTUALIZADO)
# ==========================================
class PiezaAntiguedad(models.Model):
    ESTADOS_CONSERVACION = [
        ('E', 'Excelente'),
        ('B', 'Buena'),
        ('R', 'Regular'),
        ('M', 'Mala'),
    ]
    
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la pieza")
    descripcion = models.TextField(verbose_name="Descripción detallada")
    precio = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio de venta")
    año_fabricacion = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(1950)],
        verbose_name="Año de fabricación"
    )
    estado_conservacion = models.CharField(
        max_length=1, 
        choices=ESTADOS_CONSERVACION, 
        verbose_name="Estado de conservación"
    )
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name="Fecha de ingreso")
    
    # CAMPO DE IMAGEN
    imagen = models.ImageField(
        upload_to='piezas/', 
        verbose_name="Imagen de la Pieza",
        blank=True, 
        null=True
    )

    # RELACIÓN 1:M con Proveedor
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name='piezas_proveidas',
        verbose_name="Proveedor"
    )
    
    # RELACIÓN 1:M con Cliente (comprador)
    comprador = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='piezas_compradas',
        verbose_name="Comprador"
    )
    fecha_venta = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de venta")
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Precio de venta")
    
    def __str__(self):
        return f"{self.nombre} - {self.año_fabricacion} (${self.precio})"
    
    class Meta:
        verbose_name = "Pieza de antigüedad"
        verbose_name_plural = "Piezas de antigüedad"
        ordering = ['-fecha_ingreso']

# ==========================================
# MODELOS INTERMEDIOS
# ==========================================
class ClienteProveedor(models.Model):
    TIPOS_CLIENTE = [
        ('FRECUENTE', 'Cliente Frecuente'),
        ('OCASIONAL', 'Cliente Ocasional'),
        ('MAYORISTA', 'Mayorista'),
        ('COLECCIONISTA', 'Coleccionista'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_relacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de relación")
    tipo_cliente = models.CharField(max_length=50, choices=TIPOS_CLIENTE, verbose_name="Tipo de cliente")

    class Meta:
        verbose_name = "Relación Cliente-Proveedor"
        verbose_name_plural = "Relaciones Cliente-Proveedor"
        unique_together = ['cliente', 'proveedor']

# ==========================================
# MODELO: EMPLEADO
# ==========================================
class Empleado(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    puesto = models.CharField(max_length=100, verbose_name="Puesto")
    salario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salario")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono", blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['apellido', 'nombre']

# ==========================================
# MODELO: VENTA
# ==========================================
class Venta(models.Model):
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ]

    fecha_venta = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de venta")
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total")
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, verbose_name="Método de pago")

    # RELACIONES
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='ventas',
        verbose_name="Empleado"
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='ventas',
        verbose_name="Cliente"
    )

    def __str__(self):
        return f"Venta {self.id} - {self.fecha_venta}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha_venta']

# ==========================================
# MODELO: DETALLE VENTA
# ==========================================
class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name="Venta"
    )
    pieza_antiguedad = models.ForeignKey(
        PiezaAntiguedad,
        on_delete=models.CASCADE,
        related_name='detalles_venta',
        verbose_name="Pieza de antigüedad"
    )
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio unitario")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Subtotal")
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total")

    def __str__(self):
        return f"Detalle de {self.pieza_antiguedad.nombre} en venta {self.venta.id}"

    class Meta:
        verbose_name = "Detalle de venta"
        verbose_name_plural = "Detalles de venta"
        ordering = ['venta', 'pieza_antiguedad']


