# Generated by Django 3.1.5 on 2021-01-30 08:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medidas', '0002_auto_20210130_0016'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Laboratorio',
                'verbose_name_plural': 'Laboratorios',
            },
        ),
        migrations.RemoveField(
            model_name='measure',
            name='Axis_left',
        ),
        migrations.RemoveField(
            model_name='measure',
            name='Axis_right',
        ),
        migrations.RemoveField(
            model_name='measure',
            name='Cylinder_left',
        ),
        migrations.RemoveField(
            model_name='measure',
            name='Cylinder_right',
        ),
        migrations.RemoveField(
            model_name='measure',
            name='Laboratory_name',
        ),
        migrations.RemoveField(
            model_name='measure',
            name='Price',
        ),
        migrations.RemoveField(
            model_name='measure',
            name='spherical_left',
        ),
        migrations.RemoveField(
            model_name='measure',
            name='spherical_right',
        ),
        migrations.AddField(
            model_name='measure',
            name='far_axis_left',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(180, 'El eje solo permite valores entre 0 y 180')], verbose_name='Eje izquierdo Lejos'),
        ),
        migrations.AddField(
            model_name='measure',
            name='far_axis_right',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(180, 'El eje solo permite valores entre 0 y 180')], verbose_name='Eje derecho Lejos'),
        ),
        migrations.AddField(
            model_name='measure',
            name='far_cylinder_left',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Cilindro izquierdo Lejos'),
        ),
        migrations.AddField(
            model_name='measure',
            name='far_cylinder_right',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Cilindro derecho Lejos'),
        ),
        migrations.AddField(
            model_name='measure',
            name='far_spherical_left',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Esferico izquierdo Lejos'),
        ),
        migrations.AddField(
            model_name='measure',
            name='far_spherical_right',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Esferico derecho Lejos'),
        ),
        migrations.AddField(
            model_name='measure',
            name='near_axis_left',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(180, 'El eje solo permite valores entre 0 y 180')], verbose_name='Eje izquierdo Cerca'),
        ),
        migrations.AddField(
            model_name='measure',
            name='near_axis_right',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(180, 'El eje solo permite valores entre 0 y 180')], verbose_name='Eje derecho Cerca'),
        ),
        migrations.AddField(
            model_name='measure',
            name='near_cylinder_left',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Cilindro izquierdo Cerca'),
        ),
        migrations.AddField(
            model_name='measure',
            name='near_cylinder_right',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Cilindro derecho Cerca'),
        ),
        migrations.AddField(
            model_name='measure',
            name='near_spherical_left',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Esferico izquierdo Cerca'),
        ),
        migrations.AddField(
            model_name='measure',
            name='near_spherical_right',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Esferico derecho Cerca'),
        ),
        migrations.AddField(
            model_name='measure',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Precio'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.IntegerField(blank=True, null=True, verbose_name='Edad'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='dni',
            field=models.CharField(max_length=20, unique=True, verbose_name='Dni'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Nombres'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Apellidos'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone',
            field=models.CharField(blank=True, max_length=30, verbose_name='Celular'),
        ),
        migrations.AddField(
            model_name='measure',
            name='laboratory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medidas.laboratory', verbose_name='Laboratorio'),
        ),
    ]