# Generated by Django 3.1.6 on 2021-04-11 19:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('medidas', '0007_auto_20210411_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='diagnosis',
            field=models.CharField(blank=True, help_text='Diagnostico del paciente según las medidas', max_length=84, verbose_name='Diagnostico'),
        ),
    ]
