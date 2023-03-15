# Generated by Django 3.1.6 on 2021-02-15 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medidas', '0010_auto_20210214_1853'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Laboratory',
        ),
        migrations.AddField(
            model_name='prescription',
            name='far_av_left',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Av izquierdo lejos'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='far_av_right',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Av derecho lejos'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='near_av_left',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Av izquierdo Cerca'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='near_av_right',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Av derecho Cerca'),
        ),
    ]