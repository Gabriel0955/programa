

from django import forms
from django.forms import formset_factory
from .models import Categoria,Producto , dbProveedor , Bodega , Cliente ,Venta ,Empleado ,Pago , Reporte ,ReporteVentas , Stock ,TicketCompra , ListaDeseos , VentaItem , TicketItem , DetalleFactura,Factura

class ProductoForm(forms.ModelForm):
    precio = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'imagen']


class ProveedorForm(forms.ModelForm):
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = dbProveedor
        fields = ['nombre', 'direccion', 'telefono', 'productos']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
class BodegaForm(forms.ModelForm):
    # Agrega un campo para seleccionar múltiples productos
    categoria = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Bodega
        fields = ['nombre', 'direccion', 'telefono', 'productos', 'proveedor', 'categoria']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'direccion', 'telefono', 'email']



class VentaItemForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), label='Producto')
    cantidad = forms.IntegerField(min_value=1, label='Cantidad')

VentaItemFormSet = formset_factory(VentaItemForm, extra=1)

# VentaForm using formsets
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'empleado', 'forma_pago']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create the formset using the VentaItemForm
        self.formset = VentaItemFormSet(*args, **kwargs)

    def is_valid(self):
        # Validate both the main form and the formset
        return super().is_valid() and self.formset.is_valid()

    def save(self, commit=True):
        # Save the main form instance
        venta = super().save(commit=commit)

        # Save the related VentaItemForm instances
        if commit:
            total_venta = 0  # Variable to store the total price of the entire venta
            for form in self.formset:
                producto = form.cleaned_data['producto']
                cantidad = form.cleaned_data['cantidad']

                # Calculate the total price for this VentaItem based on quantity and product price
                total_item = producto.precio * cantidad
                total_venta += total_item  # Add the item's total to the venta's total

                # Create the VentaItem instance
                item = VentaItem.objects.create(venta=venta, producto=producto, cantidad=cantidad)

            # Update the total price for the entire venta
            venta.total_precio = total_venta
            venta.save()

        return venta

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'direccion', 'telefono', 'fecha_contratacion', 'rol', 'salario']

        labels = {
            'nombre': 'Nombre',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'fecha_contratacion': 'Fecha de Contratación',
            'rol': 'Rol',
            'salario': 'Salario',
        }
        widgets = {
            'fecha_contratacion': forms.DateInput(attrs={'type': 'date'}),
        }

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['cliente','producto', 'fecha', 'metodo_pago', 'empleados','ventas']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['nombre', 'descripcion', 'archivo']

class ReporteVentasForm(forms.ModelForm):
    class Meta:
        model = ReporteVentas
        fields = ['fecha_inicio', 'fecha_fin', 'ventas']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'ventas': forms.CheckboxSelectMultiple()
        }
class AgregarStockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['producto', 'bodega', 'cantidad']

class TicketItemForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), label='Producto')
    cantidad = forms.IntegerField(min_value=1, label='Cantidad')

TicketItemFormSet = formset_factory(TicketItemForm, extra=1)

class AgregarTicketForm(forms.ModelForm):
    class Meta:
        model = TicketCompra
        fields = ['cliente', 'empleado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create the formset using the VentaItemForm
        self.formset = TicketItemFormSet(*args, **kwargs)

    def is_valid(self):
        # Validate both the main form and the formset
        return super().is_valid() and self.formset.is_valid()

    def save(self, commit=True):
        # Save the main form instance
        ticket = super().save(commit=commit)

        # Save the related VentaItemForm instances
        if commit:
            total_venta = 0  # Variable to store the total price of the entire venta
            for form in self.formset:
                producto = form.cleaned_data['producto']
                cantidad = form.cleaned_data['cantidad']

                # Calculate the total price for this VentaItem based on quantity and product price
                total_item = producto.precio * cantidad
                total_venta += total_item  # Add the item's total to the venta's total

                # Create the VentaItem instance
                item = TicketItem.objects.create(ticket=ticket, producto=producto, cantidad=cantidad)

            # Update the total price for the entire venta
            ticket.total_precio = total_venta
            ticket.save()

        return ticket

class ListaDeseosForm(forms.ModelForm):
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = ListaDeseos
        fields = ['cliente','productos']


class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = ['producto', 'precio_uni', 'cantidad']
        labels = {
            'precio_uni': 'Precio unitario',

        }


DetalleFacturaFormSet = formset_factory(DetalleFacturaForm, extra=1)

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['cliente', 'empleado', 'forma_pago']