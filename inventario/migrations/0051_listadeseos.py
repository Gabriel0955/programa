# Generated by Django 3.2.16 on 2023-07-22 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0050_ticketcompra_cantidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListaDeseos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.cliente')),
                ('productos', models.ManyToManyField(related_name='listas_deseos', to='inventario.Producto')),
            ],
        ),
    ]
