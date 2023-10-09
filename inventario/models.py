from django.db import models



class Categoria(models.Model):
    nombre = models.CharField(max_length=100)


    def __str__(self):
        return self.nombre
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    estado = models.IntegerField(default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True ,blank=True, null=True )
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class dbProveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    productos = models.ManyToManyField('Categoria', related_name='proveedores')
    estado = models.IntegerField(default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True ,blank=True, null=True )
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre



class Bodega(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    productos = models.ManyToManyField('Producto', related_name='bodegas')
    proveedor = models.ManyToManyField('dbProveedor', related_name='proveedor')
    categoria = models.ManyToManyField('Categoria', related_name='categoria')
    estado = models.IntegerField(default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True ,blank=True, null=True )
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    estado = models.IntegerField(default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True ,blank=True, null=True )
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
class RolEmpleado(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    fecha_contratacion = models.DateField()
    rol = models.ForeignKey(RolEmpleado, on_delete=models.CASCADE)
    salario = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.IntegerField(default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True ,blank=True, null=True )
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
class Venta(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    producto = models.ManyToManyField('Producto',related_name='Producto')
    fecha = models.DateTimeField(auto_now_add=True)
    empleado = models.ManyToManyField('Empleado',related_name='Empleado')
    FORMAS_DE_PAGO = (
        ('efectivo', 'Efectivo'),
        ('tarjeta_credito', 'Tarjeta de Crédito'),
        ('tarjeta_debito', 'Tarjeta de Débito'),
        ('transferencia', 'Transferencia Bancaria'),
        ('paypal', 'PayPal'),
        ('cheque', 'Cheque'),
        ('pago_movil', 'Pago Móvil'),
        ('criptomonedas', 'Criptomonedas'),
        ('pago_contra_entrega', 'Pago contra Entrega'),
        ('pago_a_plazos', 'Pago a Plazos'),
    )

    forma_pago = models.CharField(max_length=50, choices=FORMAS_DE_PAGO, null=True)
    cantidad = models.PositiveIntegerField(default=1)
    total_precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.IntegerField(default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True ,blank=True, null=True )
    fecha_modificacion = models.DateTimeField(auto_now=True)

    # Otros campos adicionales relevantes para la venta

    def __str__(self):
        # Get the first associated employee's name or display 'No empleado' if no employee is associated
        empleado_name = self.empleado.first().nombre if self.empleado.exists() else 'No empleado'
        return f'Venta {self.id} - Cliente: {self.cliente} - Empleado: {empleado_name}'
    def calcular_total(self):
        total = 0
        for item in self.items.all():
            total += item.precio
        return total

    def calcular_subtotal(self):
        subtotales = []
        for item in self.items.all():
            subtotal = item.producto.precio * item.cantidad
            subtotales.append(subtotal)

        return subtotales

class Pago(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ManyToManyField('Producto',related_name='productos')
    empleados = models.ManyToManyField('Empleado', related_name='empleado')
    ventas = models.ManyToManyField(Venta)
    fecha = models.DateField()
    metodo_pago = models.CharField(max_length=50)
    # Otros campos relacionados con el pago

    def __str__(self):
        return f"{self.cliente} - {self.fecha}"

class Reporte(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='reportes/')

    def __str__(self):
        return self.nombre

class ReporteVentas(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    ventas = models.ManyToManyField(Venta)

    def __str__(self):
        return f"Informe de Ventas del {self.fecha_inicio} al {self.fecha_fin}"




class Stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.producto} en {self.bodega} - Cantidad: {self.cantidad} "
class TicketCompra(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE)
    productos = models.ManyToManyField('Producto', related_name='pro')
    venta = models.ManyToManyField('Venta',related_name='ven')
    cantidad = models.PositiveIntegerField(default=1)
    fecha_compra = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def calcular_total(self):
        total = 0
        for item in self.ticket.all():
            total += item.precio
        return total

    # Agrega aquí otros campos adicionales relevantes para el ticket de compra, como número de factura, método de pago, etc.

    def __str__(self):
        return f'Ticket de compra {self.id} - Cliente: {self.cliente} - Fecha: {self.fecha_compra}'

class ListaDeseos(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, related_name='listas_deseos')
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'Lista de deseos de {self.cliente.nombre}'



class VentaItem(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_uni = models.FloatField(default=0)
    subtotal = models.FloatField(default=0)
    estado = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.producto} - Cantidad: {self.cantidad}"
    @property
    def precio(self):
        return self.producto.precio * self.cantidad

class TicketItem(models.Model):
    ticket = models.ForeignKey(TicketCompra, on_delete=models.CASCADE , related_name='ticket')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.ticket} - {self.producto} - Cantidad: {self.cantidad}'
    @property
    def precio(self):
        return self.producto.precio * self.cantidad
class MetodoPago(models.Model):
    forma_pago = models.CharField(max_length=50, null=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.forma_pago

class Factura(models.Model):
    fecha = models.DateField()
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE)
    venta = models.ForeignKey('Venta', on_delete=models.CASCADE)
    forma_pago = models.ManyToManyField(MetodoPago, related_name='f_pago')
    total = models.FloatField(default=0)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = "factura"
        verbose_name = "factura"
        verbose_name_plural = "facturas"

    def _str_(self):
        return f"{self.cliente}"


class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio_uni = models.FloatField(default=0)
    cantidad = models.PositiveIntegerField()
    subtotal = models.FloatField(default=0)
    estado = models.IntegerField(default=1)