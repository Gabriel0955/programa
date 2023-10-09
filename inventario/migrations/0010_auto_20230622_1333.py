# Generated by Django 3.2.16 on 2023-06-22 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0009_auto_20230622_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='imagen',
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen_url',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
    ]
