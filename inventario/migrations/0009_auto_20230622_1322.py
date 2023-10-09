# Generated by Django 3.2.16 on 2023-06-22 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0008_alter_producto_imagen_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='imagen_url',
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='media'),
        ),
    ]
