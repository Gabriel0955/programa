# Generated by Django 3.2.16 on 2023-06-22 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0011_alter_producto_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='imagen_url',
            new_name='imagen',
        ),
        migrations.AlterField(
            model_name='producto',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]