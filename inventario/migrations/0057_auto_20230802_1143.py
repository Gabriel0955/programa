# Generated by Django 3.2.16 on 2023-08-02 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0056_auto_20230801_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='total_precio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]