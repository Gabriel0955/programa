# Generated by Django 3.2.16 on 2023-07-20 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0049_auto_20230720_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketcompra',
            name='cantidad',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
