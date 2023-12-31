# Generated by Django 3.2.16 on 2023-07-24 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0052_auto_20230724_1113'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.producto')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.ticketcompra')),
            ],
        ),
    ]
