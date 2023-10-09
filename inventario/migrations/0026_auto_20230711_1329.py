# Generated by Django 3.2.16 on 2023-07-11 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0025_venta_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='bodega',
            name='estado',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='cliente',
            name='estado',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='dbproveedor',
            name='estado',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='detalleventa',
            name='estado',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='producto',
            name='estado',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='venta',
            name='estado',
            field=models.IntegerField(default=1),
        ),
    ]