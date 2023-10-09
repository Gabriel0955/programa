# Generated by Django 3.2.16 on 2023-08-01 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0054_auto_20230731_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio_uni', models.FloatField(default=0)),
                ('cantidad', models.PositiveIntegerField()),
                ('subtotal', models.FloatField(default=0)),
                ('estado', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('total', models.FloatField(default=0)),
                ('estado', models.IntegerField(default=1)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.cliente')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.empleado')),
            ],
            options={
                'verbose_name': 'factura',
                'verbose_name_plural': 'facturas',
                'db_table': 'factura',
            },
        ),
        migrations.AddField(
            model_name='factura',
            name='venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.venta'),
        ),
        migrations.AddField(
            model_name='detallefactura',
            name='factura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.factura'),
        ),
        migrations.AddField(
            model_name='detallefactura',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.producto'),
        ),
    ]
