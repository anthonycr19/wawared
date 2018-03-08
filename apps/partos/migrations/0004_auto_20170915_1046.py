# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('partos', '0003_auto_20170529_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='partogramamedicion',
            name='medicamentos',
            field=models.TextField(null=True, verbose_name='Medicamentos', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partogramamedicion',
            name='orina_cetona',
            field=models.CharField(max_length=100, null=True, verbose_name='Cetonas', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partogramamedicion',
            name='orina_proteinas',
            field=models.CharField(blank=True, max_length=10, verbose_name='Prote\xednas', choices=[('+', '+'), ('++', '++'), ('+++', '+++')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partogramamedicion',
            name='orina_volumen',
            field=models.FloatField(null=True, verbose_name='Volumen', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partogramamedicion',
            name='tv_membranas_rotas_tiempo',
            field=models.FloatField(blank=True, null=True, verbose_name='Tiempo', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(48)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='duracion_parto_perdiodo_1',
            field=models.FloatField(blank=True, null=True, verbose_name='1er periodo', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(48)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='duracion_parto_perdiodo_2',
            field=models.FloatField(blank=True, null=True, verbose_name='2do periodo', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(48)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='duracion_parto_perdiodo_3',
            field=models.FloatField(blank=True, null=True, verbose_name='3er periodo', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(48)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partogramamedicion',
            name='du_duracion',
            field=models.CharField(blank=True, max_length=20, verbose_name='Duraci\xf3n', choices=[('-20', 'menos de 20'), ('20 - 40', '20 a 40'), ('40+', '40 a mas')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partogramamedicion',
            name='tv_descenso_cefalico',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Descenso cef\xe1lico', choices=[('0', '5/5 || -4'), ('1', '4/5 || -3'), ('2', '3/5 || -2'), ('3', '2/5 || -1/0'), ('4', '1/5 || +1/+2'), ('5', '0/5 || +3/+4')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partogramamedicion',
            name='tv_membranas_rotas_tipo',
            field=models.CharField(blank=True, max_length=10, verbose_name='Tipo', choices=[('artificial', 'Artificial'), ('espontanea', 'Espontanea')]),
            preserve_default=True,
        ),
    ]
