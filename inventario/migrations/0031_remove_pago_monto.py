# Generated by Django 3.2.16 on 2023-07-12 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0030_pago_producto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pago',
            name='monto',
        ),
    ]
