# Generated by Django 3.2.16 on 2023-07-09 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0024_cliente_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='producto',
            field=models.ManyToManyField(related_name='Producto', to='inventario.Producto'),
        ),
    ]
