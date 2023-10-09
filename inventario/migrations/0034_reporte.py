# Generated by Django 3.2.16 on 2023-07-14 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0033_pago_empleados'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('archivo', models.FileField(upload_to='reportes/')),
            ],
        ),
    ]
