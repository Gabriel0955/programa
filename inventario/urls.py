from django.contrib import admin
from django.urls import path
from . import views
from .views import ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView , ReporteClientesPDFView
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    #crud para bodega

    path('eliminar_bodega/', views.eliminar_bodega, name='eliminar_bodega'),
    path('modificar_bodega/', views.modificar_bodega, name='modificar_bodega'),
    #crud para ventas
    path('consultar_carrito/', views.consultar_carrito, name='consultar_carrito'),
    path('crear_carrito/', views.crear_carrito, name='crear_carrito'),
    path('eliminar_carrito/', views.eliminar_carrito, name='eliminar_carrito'),
    path('modificar_carrito/', views.modificar_carrito, name='modificar_carrito'),
    #crud para productos

    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('eliminar_producto/', views.eliminar_producto, name='eliminar_producto'),
    path('modificar_producto/', views.modificar_producto, name='modificar_producto'),
    #crud para usuarios

    #crud para producto
    path('lista_productos/',views.lista_productos),
    path('consultar_producto/', views.consultar_producto, name='consultar_producto'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('inventario/eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('modificar/<int:producto_id>/', views.modificar_producto, name='modificar_producto'),
    #crud para proveedores
    path('consultar_proveedor/',views.consultar_proveedor, name='consultar_proveedor'),
    path('crear_proveedor/',views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/<int:proveedor_id>/modificar/', views.modificar_proveedor, name='modificar_proveedor'),
    path('proveedores/<int:proveedor_id>/eliminar/', views.eliminar_proveedor, name='eliminar_proveedor'),

    #crud para bodega
    path('consultar_bodega/',views.consultar_bodega, name='consultar_bodega'),
    path('crear_bodega/',views.agregar_bodega, name='crear_bodega'),
    path('bodega/<int:bodega_id>/modificar/', views.modificar_bodega, name='modificar_bodega'),
    path('bodega/<int:bodega_id>/eliminar/', views.eliminar_bodega, name='eliminar_bodega'),
    #crud para cliente


    path('clientes/', ClienteListView.as_view(), name='consultar_cliente'),
    path('clientes/', ClienteListView.as_view(), name='lista_clientes'),
    path('clientes/nuevo/', ClienteCreateView.as_view(), name='nuevo_cliente'),
    path('clientes/<int:pk>/editar/', ClienteUpdateView.as_view(), name='editar_cliente'),
    path('clientes/<int:pk>/eliminar/', ClienteDeleteView.as_view(), name='eliminar_cliente'),
    path('generar-reporte/', ReporteClientesPDFView.as_view(), name='generar_reporte_clientes'),




    # crud para venta
    path('consultar_venta/<int:venta_id>/', views.consultar_venta, name='consultar_venta'),
    path('crear_venta/',views.crear_venta, name='crear_venta'),



    # crud para empleado
    path('consultar_empleado/', views.mostrar_empleados, name='mostrar_empleados'),
    path('agregar_empleado/',views.agregar_empleado, name='agregar_empleado'),
    path('empleados/modificar/<int:empleado_id>/', views.modificar_empleado, name='modificar_empleado'),
    path('empleados/eliminar/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'),
    #crud de pago
    path('agregar_pago/', views.registrar_pago, name='agregar_pago'),
    path('consultar_pago/', views.mostrar_pagos, name='consultar_pago'),
    path('venta/<int:venta_id>/', views.eliminar_pago, name='eliminar_pago'),
    #crud de reporte
    path('consultar_reporte/', views.listar_reportes, name='listar_reportes'),
    path('reportes/agregar/', views.agregar_reporte, name='agregar_reporte'),
    #crud de reporte de venta
    path('agregar_rventa/', views.agregar_reporte_venta, name='agregar_rventa'),
    path('consultar_rventa/', views.consultar_rventa, name='consultar_rventa'),

    path('detalle_venta/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    path('ver_stock/', views.ver_stock, name='ver_stock'),
    path('agregar_stock/', views.registrar_stock, name='agregar_stock'),
    path('stock/modificar/<int:stock_id>/', views.modificar_stock, name='modificar_stock'),
    path('stock/eliminar/<int:stock_id>/', views.eliminar_stock, name='eliminar_stock'),

    path('consultar_ticket/',views.mostrar_tickets,name='mostrar_ticket'),
    path('agregar_ticket/', views.crear_ticket, name='crear_ticket'),
    path('ticket/eliminar/<int:ticket_id>/', views.eliminar_ticket, name='eliminar_ticket'),

    path('generar_reporte_pdf/', views.generar_reporte_pdf, name='generar_reporte_pdf'),
    path('consultar_venta/<int:venta_id>/pdf/', views.consultar_venta_pdf, name='consultar_venta_pdf'),
    path('consultar_ticket/<int:ticket_id>/pdf/', views.generar_pdf_ticket, name='generar_pdf_ticket'),

    path('consultar_lista/', views.detalle_lista_deseos, name='detalle_lista_deseos'),
    path('agregar_lista/', views.registrar_lista, name='registrar_lista'),
    path('lista/eliminar/<int:lista_id>/', views.eliminar_lista, name='eliminar_lista'),
    path('lista/modificar/<int:lista_id>/', views.modificar_lista, name='modificar_lista'),
    path('crear_factura/', views.create_factura, name='crear_factura'),





]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)