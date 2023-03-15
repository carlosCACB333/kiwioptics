# Generated by Django 3.1.6 on 2021-02-15 19:51

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medidas', '0011_auto_20210215_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='gender',
            field=models.CharField(blank=True, choices=[('Masculino', 'Male'), ('Femenino', 'Female'), ('Otro', 'Other')], max_length=20, verbose_name='Genero'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='price',
            field=models.DecimalField(choices=[(Decimal('0.1'), '0.1'), (1.1, 'Normal'), (2.2, 'High')], decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0, 'No se permite el valor ingresado')], verbose_name='Precio'),
        ),
    ]