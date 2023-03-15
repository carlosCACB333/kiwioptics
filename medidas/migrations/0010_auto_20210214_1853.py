# Generated by Django 3.1.5 on 2021-02-14 23:53

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medidas', '0009_auto_20210213_1947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='add',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='dip',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='laboratory',
        ),
        migrations.AddField(
            model_name='prescription',
            name='far_dip',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='DIP lejos'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='intermediate_add',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='ADD intermedio'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='near_add',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='ADD cerca'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='near_dip',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='DIP cerca'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='far_axis_left',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(180, 'El eje solo permite valores entre 0° y 180°')], verbose_name='Eje izquierdo Lejos'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='far_axis_right',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(180, 'El eje solo permite valores entre 0° y 180°')], verbose_name='Eje derecho Lejos'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='near_axis_right',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(180, 'El eje solo permite valores entre 0° y 180°')], verbose_name='Eje derecho Cerca'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0, 'No se permite el valor ingresado')], verbose_name='Precio'),
        ),
    ]