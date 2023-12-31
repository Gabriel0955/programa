# Generated by Django 3.2.16 on 2023-07-09 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0022_cliente_detalleventa_venta'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='detalleventa',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='detalleventa',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='venta',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='venta',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
