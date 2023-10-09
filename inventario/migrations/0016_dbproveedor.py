# Generated by Django 3.2.16 on 2023-07-03 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0015_alter_producto_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='dbProveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('productos', models.ManyToManyField(related_name='proveedores', to='inventario.Producto')),
            ],
        ),
    ]