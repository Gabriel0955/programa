# Generated by Django 3.2.16 on 2023-07-20 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0042_auto_20230720_0043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facturas',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='facturas',
            name='metodo_pago',
        ),
        migrations.AddField(
            model_name='venta',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
        migrations.DeleteModel(
            name='DetalleFacturas',
        ),
        migrations.DeleteModel(
            name='Facturas',
        ),
    ]