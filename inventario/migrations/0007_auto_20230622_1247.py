# Generated by Django 3.2.16 on 2023-06-22 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0006_auto_20230622_1232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='imagen',
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
