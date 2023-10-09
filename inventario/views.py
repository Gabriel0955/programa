from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from reportlab.pdfgen import canvas
from django.contrib.auth import logout
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from django.views.generic import ListView , CreateView , UpdateView , DeleteView , View
from django.urls import reverse_lazy
from django.http import HttpResponse
import io
import os
import json
from PIL import Image as PILImage
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import qrcode
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from django.conf import settings
from reportlab.platypus import Image
from inventario.models import Producto, Categoria, dbProveedor, Bodega, Cliente, Venta, Empleado, RolEmpleado, Pago, \
    Reporte, ReporteVentas, Stock, TicketCompra , ListaDeseos , VentaItem ,TicketItem , Factura,DetalleFactura
from .forms import ProductoForm, ProveedorForm, BodegaForm, ClienteForm, VentaForm, EmpleadoForm, PagoForm, ReporteForm, \
    ReporteVentasForm, AgregarStockForm, AgregarTicketForm , ListaDeseosForm , VentaItemFormSet , TicketItemFormSet , DetalleFactura , DetalleFacturaFormSet , FacturaForm


# Create your views here.

# crud para ventas
def consultar_carrito(request):
    return render(request, 'ventas/consultar_venta.html')


def crear_carrito(request):
    return render(request, 'ventas/crear_venta.html')


def eliminar_carrito(request):
    return render(request, 'ventas/eliminar_venta.html')


def modificar_carrito(request):
    return render(request, 'ventas/modificar_venta.html')


# crud para productos

def crear_producto(request):
    return render(request, 'productos/agregar_productos.html')


# crud para usuarios

def crear_usuario(request):
    return render(request, 'usuarios/crear_usuario.html')


def eliminar_usuario(request):
    return render(request, 'usuarios/eliminar_usuario.html')


def modificar_usuario(request):
    return render(request, 'usuarios/modificar_usuario.html')


def lista_productos(request):
    # Obtener el término de búsqueda ingresado en el formulario
    search_term = request.GET.get('search')

    # Filtrar los productos por nombre si hay un término de búsqueda
    if search_term:
        productos = Producto.objects.filter(nombre__icontains=search_term)
    else:
        productos = Producto.objects.all()

    context = {
        'productos': productos,
    }
    return render(request, 'productos/consultar_productos.html', context)

def consultar_producto(request):
    categorias = Categoria.objects.all()
    search_term = request.GET.get('search')
    categoria_id = request.GET.get('categoria')

    # Inicializar el queryset de productos
    productos = Producto.objects.all()

    if search_term:
        try:
            # Intentar convertir el valor ingresado a un número (ID de producto)
            producto_id = int(search_term)
            # Si se puede convertir, filtrar por ID de producto
            productos = productos.filter(id=producto_id)
        except ValueError:
            # Si no se puede convertir, filtrar por nombre de producto
            productos = productos.filter(nombre__icontains=search_term)

    # Filtrar los productos por ID de categoría si hay una categoría seleccionada
    if categoria_id:
        productos = productos.filter(categoria__id=categoria_id)

    context = {
        'categorias': categorias,
        'productos': productos,
    }
    return render(request, 'productos/consultar_productos.html', context)


def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('consultar_producto')
    else:
        form = ProductoForm()

    categorias = Categoria.objects.all()
    context = {
        'form': form,
        'categorias': categorias,
    }

    return render(request, 'productos/agregar_productos.html', context)


def eliminar_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    producto.delete()
    return redirect('consultar_producto')


def modificar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('consultar_producto')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/modificar_productos.html',
                  {'form': form, 'producto': producto, 'categorias': categorias})


def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('consultar_proveedor')
    else:
        form = ProveedorForm()
    productos = Categoria.objects.all()

    context = {
        'form': form,
        'productos': productos,
    }

    return render(request, 'proveedor/crear_proveedor.html', context)


def consultar_proveedor(request):
    search_term = request.GET.get('search')

    if search_term:
        proveedores = dbProveedor.objects.filter(nombre__icontains=search_term)
    else:
        proveedores = dbProveedor.objects.all()

    context = {
        'proveedores': proveedores,
    }
    return render(request, 'proveedor/consultar_proveedor.html', context)


def eliminar_proveedor(request, proveedor_id):
    proveedor = dbProveedor.objects.get(id=proveedor_id)
    proveedor.delete()
    return redirect('consultar_proveedor')


def modificar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(dbProveedor, id=proveedor_id)
    categorias = Categoria.objects.all()
    producto = Producto.objects.all()

    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('consultar_proveedor')
    else:
        form = ProveedorForm(instance=proveedor)
        form.fields[
            'productos'].queryset = Categoria.objects.all()  # Agrega esta línea para pasar los productos al formulario

    return render(request, 'proveedor/modificar_proveedor.html',
                  {'form': form, 'proveedor': proveedor, 'categorias': categorias, 'producto':producto})


def consultar_bodega(request):
    search_term = request.GET.get('search')

    if search_term:
        bodega = Bodega.objects.filter(nombre__icontains=search_term)
    else:
        bodega = Bodega.objects.all()

    context = {
        'bodega': bodega,
    }
    return render(request, 'bodega/consultar_bodega.html', context)


def agregar_bodega(request):
    if request.method == 'POST':
        form = BodegaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('consultar_bodega')
    else:
        form = BodegaForm()
    productos = Categoria.objects.all()
    proveedor = dbProveedor.objects.all()

    context = {
        'form': form,
        'productos': productos,
        'proveedor': proveedor,
    }

    return render(request, 'bodega/crear_bodega.html', context)


def eliminar_bodega(request, bodega_id):
    bodega = get_object_or_404(Bodega, id=bodega_id)
    bodega.delete()
    return redirect('consultar_bodega')


def modificar_bodega(request, bodega_id):
    bodega = get_object_or_404(Bodega, id=bodega_id)
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        form = BodegaForm(request.POST, instance=bodega)
        if form.is_valid():
            form.save()
            return redirect('consultar_bodega')
    else:
        form = BodegaForm(instance=bodega)
        form.fields[
            'productos'].queryset = Producto.objects.all()  # Asegúrate de ajustar el queryset según tus necesidades

    return render(request, 'bodega/modificar_bodega.html', {'form': form, 'bodega': bodega, 'categorias': categorias})


class ClienteListView(ListView):
    model = Cliente
    template_name = 'usuarios/consultar_cliente.html'
    context_object_name = 'clientes'


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'usuarios/crear_usuario.html'
    success_url = reverse_lazy('consultar_cliente')


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'usuarios/eliminar_usuario.html'
    success_url = reverse_lazy('consultar_cliente')


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'usuarios/modificar_usuario.html'
    success_url = reverse_lazy('consultar_cliente')


class ReporteClientesPDFView(View):
    def get(self, request, *args, **kwargs):
        # Crear un objeto PDF
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)

        # Establecer el título del reporte con estilo centrado y fuente grande
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawCentredString(400, 800, "Reporte de Clientes")

        # Obtener datos de clientes para el reporte desde la base de datos
        clientes = Cliente.objects.all()

        # Crear una lista para almacenar los datos de clientes
        data = [
            ["Nombre", "Dirección", "Teléfono", "Email", "Fecha de creación"]
        ]
        for cliente in clientes:
            data.append([
                cliente.nombre,
                cliente.direccion,
                cliente.telefono,
                cliente.email,
                str(cliente.fecha_creacion)
            ])

        # Establecer estilos para el PDF
        styles = getSampleStyleSheet()
        style_data = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Color de fondo para el encabezado
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Color de texto para el encabezado
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alineación del texto a la izquierda
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Agregar bordes a todas las celdas
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente general
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Estilo de la fila de encabezado
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Espacio inferior de las celdas
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Color de fondo para filas alternas
        ]

        # Crear la tabla con los datos y aplicar los estilos
        table = Table(data, colWidths=[120, 180, 80, 180, 120], repeatRows=1)
        table.setStyle(TableStyle(style_data))

        # Dibujar la tabla en el PDF
        table.wrapOn(pdf, 400, 200)
        table.drawOn(pdf, 72, 600)

        # Agregar encabezado y pie de página con estilo
        pdf.setFont("Helvetica", 10)
        pdf.drawString(72, 40, "www.tuempresa.com - Teléfono: +123456789")
        pdf.drawString(400, 40, "Página 1")

        # Finalizar el PDF
        pdf.save()

        # Obtener el contenido del PDF desde el buffer
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_clientes.pdf"'
        return response
def consultar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    producto = venta.producto.all()
    context = {
        'venta': venta,
        'producto': producto,
    }

    return render(request, 'ventas/consultar_venta.html', context)


def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=True)

            # Save the related VentaItemForm instances from the formset
            for formset_form in form.formset:
                producto = formset_form.cleaned_data.get('producto')
                cantidad = formset_form.cleaned_data.get('cantidad')
                if producto and cantidad:
                    existing_item = VentaItem.objects.filter(venta=venta, producto=producto).first()
                    if existing_item:
                        existing_item.cantidad = cantidad
                        existing_item.save()
                    else:
                        VentaItem.objects.create(venta=venta, producto=producto, cantidad=cantidad)

            return redirect('consultar_venta', venta_id=venta.id)
    else:
        form = VentaForm()
        form.formset = VentaItemFormSet()

    return render(request, 'ventas/crear_venta.html', {'form': form})



def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    producto = Producto.objects.all()
    cliente = Cliente.objects.all()
    empleado = Empleado.objects.all()

    context = {
        'venta': venta,
        'producto': producto,
        'cliente': cliente,
        'empleado': empleado,
    }

    return render(request, 'ventas/detalle_venta.html', context)


def mostrar_empleados(request):
    search_term = request.GET.get('search')

    if search_term:
        empleados = Empleado.objects.filter(nombre__icontains=search_term)
    else:
        empleados = Empleado.objects.all()

    context = {
        'empleados': empleados,
    }
    return render(request, 'empleados/consultar_empleado.html', context)


def agregar_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mostrar_empleados')
    else:
        form = EmpleadoForm()
    roles = RolEmpleado.objects.all()

    context = {
        'form': form,
        'roles': roles,
    }

    return render(request, 'empleados/crear_empleado.html', context)


def modificar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('mostrar_empleados')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'empleados/modificar_empleado.html', {'form': form, 'empleado': empleado})


def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    empleado.delete()
    return redirect('mostrar_empleados')


def mostrar_pagos(request):
    search_query = request.GET.get('search')
    pagos = Pago.objects.all()
    productos = Producto.objects.all()

    if search_query:
        pagos = pagos.filter(
            Q(cliente__nombre__icontains=search_query) |
            Q(producto__nombre__icontains=search_query)
        ).distinct()

    clientes = Cliente.objects.all()
    venta = Venta.objects.all()

    context = {
        'pagos': pagos,
        'productos': productos,
        'clientes': clientes,
        'venta': venta,
    }

    return render(request, 'pago/consultar_pago.html', context)


def registrar_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consultar_pago')
    else:
        form = PagoForm()
    producto = Producto.objects.all()
    cliente = Cliente.objects.all()
    empleado = Empleado.objects.all()

    context = {
        'form': form,
        'producto': producto,
        'cliente': cliente,
        'empleado': empleado,
    }
    return render(request, 'pago/agregar_pago.html', context)


def eliminar_pago(request, venta_id):
    pago = get_object_or_404(Venta, id=venta_id)
    pago.delete()
    return redirect('consultar_pago')


def listar_reportes(request):
    reportes = Reporte.objects.all()
    return render(request, 'reporte/consultar_reporte.html', {'reportes': reportes})


def agregar_reporte(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_reportes')
    else:
        form = ReporteForm()
    return render(request, 'reporte/agregar_reporte.html', {'form': form})


def agregar_reporte_venta(request):
    if request.method == 'POST':
        form = ReporteVentasForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('consultar_rventa')
    else:
        form = ReporteForm()
    return render(request, 'reporte_venta/agregar_rventa.html', {'form': form})


def consultar_rventa(request):
    reporte_venta = ReporteVentas.objects.all()
    ventas = Venta.objects.all()

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        ventas = ventas.filter(fecha__range=[fecha_inicio, fecha_fin])

    return render(request, 'reporte_venta/consultar_rventa.html', {'ventas': ventas, 'reporte_venta': reporte_venta})


def ver_stock(request):
    stock = Stock.objects.all()
    producto = Producto.objects.all()
    bodega = Bodega.objects.all()

    # Obtener el término de búsqueda del formulario
    search_query = request.GET.get('search')
    if search_query:
        # Filtrar el stock según el término de búsqueda
        stock = stock.filter(producto__nombre__icontains=search_query)

    return render(request, 'stock/consultar_stock.html', {'stock': stock, 'producto': producto, 'bodega': bodega})


def registrar_stock(request):
    if request.method == 'POST':
        form = AgregarStockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_stock')
    else:
        form = AgregarStockForm()
    producto = Producto.objects.all()
    bodega = Bodega.objects.all()

    context = {
        'form': form,
        'producto': producto,
        'bodega': bodega,
    }
    return render(request, 'stock/crear_stock.html', context)


def modificar_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        form = AgregarStockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('ver_stock')
    else:
        form = AgregarStockForm(instance=stock)
    return render(request, 'stock/modificar_stock.html', {'form': form})


def eliminar_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    stock.delete()
    return redirect('ver_stock')



def crear_ticket(request):
    if request.method == 'POST':
        form = AgregarTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=True)

            # Save the related VentaItemForm instances from the formset
            for formset_form in form.formset:
                producto = formset_form.cleaned_data.get('producto')
                cantidad = formset_form.cleaned_data.get('cantidad')
                if producto and cantidad:
                    existing_item = TicketItem.objects.filter(ticket=ticket, producto=producto).first()
                    if existing_item:
                        existing_item.cantidad = cantidad
                        existing_item.save()
                    else:
                        VentaItem.objects.create(ticket=ticket, producto=producto, cantidad=cantidad)

            return redirect('mostrar_ticket')
    else:
        form = AgregarTicketForm()
        form.formset = TicketItemFormSet()

    return render(request, 'ticket/crear_ticket.html', {'form': form})

def mostrar_tickets(request):
    tickets = TicketCompra.objects.all()
    producto = Producto.objects.all()

    # Obtener el término de búsqueda del formulario
    search_query = request.GET.get('search')
    if search_query:
        # Filtrar los tickets por clientes o productos que coincidan con el término de búsqueda
        tickets = tickets.filter(
            Q(cliente__nombre__icontains=search_query) |
            Q(productos__nombre__icontains=search_query)
        ).distinct()

    return render(request, 'ticket/consultar_ticket.html', {'tickets': tickets, 'producto': producto})


def eliminar_ticket(request, ticket_id):
    ticket = get_object_or_404(TicketCompra, id=ticket_id)
    ticket.delete()
    return redirect('mostrar_ticket')


def generar_reporte_pdf(request):
    # Obtener los datos de ventas desde la base de datos
    reporte_venta = ReporteVentas.objects.all()
    ventas = Venta.objects.all()

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        ventas = ventas.filter(fecha__range=[fecha_inicio, fecha_fin])

    # Crear un buffer para el PDF
    buffer = io.BytesIO()

    # Crear un documento PDF utilizando SimpleDocTemplate
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Crear una lista para almacenar los datos de ventas en forma de tabla
    data = [['ID', 'Fecha', 'Cliente', 'Producto', 'Cantidad', 'Precio Unitario', 'Total']]

    for venta in ventas:
        # Crear listas para almacenar los productos, las cantidades y los precios de cada venta
        productos = []
        cantidades = []
        precios_unitarios = []
        total_venta = 0

        # Iterar sobre los productos asociados a la venta actual
        for item in venta.items.all():
            producto_nombre = item.producto.nombre
            cantidad = item.cantidad
            precio_unitario = item.producto.precio
            total_item = cantidad * precio_unitario

            productos.append(producto_nombre)
            cantidades.append(cantidad)
            precios_unitarios.append(precio_unitario)
            total_venta += total_item

        # Crear una lista con los datos de la venta y agregarla a la lista 'data'
        data.append([venta.id, venta.fecha, venta.cliente.nombre, ', '.join(productos), ', '.join(map(str, cantidades)),
                     ', '.join(map(str, precios_unitarios)), total_venta])

    # Crear una tabla con los datos de ventas
    table = Table(data)

    # Establecer el estilo de la tabla
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Agregar la tabla al documento
    elements = [table]

    # Construir el documento y cerrar el buffer
    doc.build(elements)
    buffer.seek(0)

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'
    return response


def consultar_venta_pdf(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="venta_{venta_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Obtener la ruta absoluta de la imagen
    image_filename = "../media/productos/2.png"
    image_path = os.path.join(settings.MEDIA_ROOT, image_filename)

    # Verificar que el archivo de imagen exista
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"La imagen '{image_filename}' no se encontró en la ruta '{image_path}'.")

    # Agregar imagen al PDF
    logo = Image(image_path, width=150, height=100)
    elements.append(logo)
    elements.append(Paragraph('Factura de Venta', styles['Title']))
    if venta.empleado.exists():
        empleado_name = venta.empleado.first().nombre

    else:
        empleado_name = 'No empleado'
    # Add venta information to the PDF

    # Seller information (Replace the placeholders with actual seller details)
    elements.append(Paragraph(f'Vendedor: {empleado_name}', styles['Normal']))
    elements.append(Paragraph('Empresa: BOUTIQUE HG', styles['Normal']))
    elements.append(Paragraph('Dirección de la empresa: NUEVE DE OCTUBRE', styles['Normal']))
    elements.append(Paragraph('Ciudad, Código Postal: GUAYAQUIL,090150', styles['Normal']))
    elements.append(Paragraph('Teléfono:(04)316-6072', styles['Normal']))
    elements.append(Spacer(1, 12))  # Add some space between sections

    # Buyer information (Replace the placeholders with actual buyer details)
    elements.append(Paragraph('Datos del Comprador:', styles['Heading1']))
    elements.append(Paragraph(f'Nombre del cliente: {venta.cliente}', styles['Normal']))
    elements.append(Paragraph(f'Dirección del cliente: {venta.cliente.email}', styles['Normal']))
    elements.append(Paragraph(f'Ciudad: Guayaquil', styles['Normal']))
    elements.append(Paragraph(f'Telefono: {venta.cliente.telefono}', styles['Normal']))
    elements.append(Spacer(1, 12))  # Add some space between sections

    # Invoice details
    elements.append(Paragraph('Detalles de la Factura:', styles['Heading1']))
    elements.append(Paragraph(f'Número de Factura: {venta.id}', styles['Normal']))
    elements.append(Paragraph(f'Metodo de pago: {venta.forma_pago}', styles['Normal']))
    elements.append(Paragraph(f'Fecha de emisión: {venta.fecha.strftime("%d/%m/%Y")}', styles['Normal']))
    elements.append(Spacer(1, 12))  # Add some space between sections
    # Table with product information
    data = [['Id','Producto', 'Cantidad', 'Precio Unitario', 'Subtotal']]
    total = 0
    for item in venta.items.all():
        subtotal = item.producto.precio * item.cantidad
        total += subtotal
        data.append([item.producto.id,item.producto.nombre, item.cantidad, f'${item.producto.precio:.2f}', f'${subtotal:.2f}'])
    data.append(['', '','', 'Total:', f'${total:.2f}'])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    # Build the PDF document
    doc.build(elements)

    return response


def generar_pdf_ticket(request, ticket_id):
    ticket = get_object_or_404(TicketCompra, id=ticket_id)

    # Serialize ticket information to JSON
    ticket_data = {
        'ticket_id': ticket_id,
        'cliente': ticket.cliente.nombre,
        'productos': [
            {
                'identificador': item.producto.id,
                'producto': item.producto.nombre,
                'cantidad': item.cantidad,
                'precio': "{:.2f}".format(float(item.producto.precio)),  # Format price with 2 decimals
                'subtotal': "{:.2f}".format(float(item.precio)),  # Format subtotal with 2 decimals
            } for item in ticket.ticket.all()
        ],
    }

    # Calculate the total amount
    total = sum(float(item['subtotal']) for item in ticket_data['productos'])
    ticket_data['total'] = "{:.2f}".format(total)  # Format total with 2 decimals

    # Add a custom message with the client's name to the QR code
    qr_message = f"Gracias por su compra, {ticket.cliente.nombre}"
    ticket_data['qr_message'] = qr_message

    # Convert ticket_data to JSON string
    ticket_data_json = json.dumps(ticket_data)

    # Generate the QR code
    qr_code = qrcode.make(ticket_data_json)

    # Resize the QR code image to fit within the frame
    max_image_size = 150
    qr_code.thumbnail((max_image_size, max_image_size), PILImage.ANTIALIAS)

    # Add the QR code image to the PDF
    qr_code_image_io = BytesIO()
    qr_code.save(qr_code_image_io, format='PNG')
    qr_code_image = Image(qr_code_image_io)

    # Create the PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket_id}.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1, parent=styles['Normal']))

    # Contenido del PDF
    story = []
    story.append(Paragraph(f'Ticket de Compra #{ticket_id}', styles['Title']))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f'Cliente: {ticket.cliente.nombre}', styles['Title']))
    story.append(Spacer(1, 10))

    data = [['Identificador', 'Producto', 'Cantidad', 'Precio', 'Subtotal']]

    for item in ticket_data['productos']:
        data.append([item['identificador'], item['producto'], item['cantidad'], item['precio'], item['subtotal']])

    data.append(['', '', '', 'Total:', ticket_data['total']])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))

    story.append(table)
    story.append(Spacer(1, 30))
    story.append(Paragraph(f'Total: ${ticket_data["total"]}', styles['Title']))
    story.append(Paragraph('Nota: Acérquese a la tienda con este ticket para agilizar la compra', styles['Heading5']))

    # Add the custom QR code message to the story
    story.append(Paragraph(f'{ticket_data["qr_message"]}', styles['Heading5']))

    # Add the QR code image to the story
    story.append(qr_code_image)

    doc.build(story)

    return response

def detalle_lista_deseos(request):
    lista = ListaDeseos.objects.all()
    return render(request, 'lista_deseos/consultar_lista.html', {'lista': lista})

def modificar_lista(request, lista_id):
    lista = get_object_or_404(ListaDeseos, id=lista_id)
    if request.method == 'POST':
        form = ListaDeseosForm(request.POST, instance=lista)
        if form.is_valid():
            form.save()
            return redirect('detalle_lista_deseos')
    else:
        form = ListaDeseosForm(instance=lista)
    return render(request, 'lista_deseos/modificar_lista.html', {'form': form, 'lista': lista})

def registrar_lista(request):
    if request.method == 'POST':
        form = ListaDeseosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detalle_lista_deseos')
    else:
        form = ListaDeseosForm()
    producto = Producto.objects.all()
    cliente = Cliente.objects.all()


    context = {
        'form': form,
        'producto': producto,
        'cliente':cliente,

    }
    return render(request, 'lista_deseos/crear_lista.html', context)

def eliminar_lista(request, lista_id):
    lista = get_object_or_404(ListaDeseos, id=lista_id)
    lista.delete()
    return redirect('detalle_lista_deseos')


def create_factura(request):
    form = FacturaForm()

    formset = DetalleFacturaFormSet()
    if request.method == "POST":
        form = FacturaForm(request.POST)
        formset = DetalleFacturaFormSet(request.POST)
        if form.is_valid():
            factura = Factura.objects.create(
                fecha=form.cleaned_data["fecha"],
                cliente=form.cleaned_data["cliente"],
                empleado=form.cleaned_data["empleado"],
                metodo_pago=form.cleaned_data["metodo_pago"],
            )
        if formset.is_valid():
            total = 0
            for form in formset:
                producto = form.cleaned_data["producto"]
                cantidad = form.cleaned_data["cantidad"]
                precio_uni = form.cleaned_data["precio_uni"]
                if producto and cantidad:
                    suma = float(precio_uni) * float(cantidad)
                    total += suma

                    DetalleFactura(
                        factura=factura, producto=producto, cantidad=cantidad, precio_uni=precio_uni, subtotal=suma
                    ).save()

            factura.total = total
            factura.save()
            return redirect("consultar_venta")
    context = {

        "form": form,
        "formset": formset,
    }

    return render(request, "factura/crear_factura.html", context)