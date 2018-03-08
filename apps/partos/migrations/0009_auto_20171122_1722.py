# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('partos', '0008_placenta_liquido_amniotico_otras_caracteristicas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placenta',
            name='cordon_umbilical_diametro',
            field=models.IntegerField(blank=True, null=True, verbose_name='Diametro', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='placenta',
            name='cordon_umbilical_longitud',
            field=models.IntegerField(blank=True, null=True, verbose_name='Longitud', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='placenta',
            name='liquido_amniotico_cantidad',
            field=models.IntegerField(blank=True, null=True, verbose_name='Cantidad', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='placenta',
            name='liquido_amniotico_color',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Color', choices=[('claro', 'Claro'), ('meconial', 'Meconial'), ('sanguinolento', 'Sanguinolento')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='placenta',
            name='liquido_amniotico_olor',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Olor', choices=[('sui generis', 'Sui generis'), ('Otros', 'Otros')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='placenta',
            name='membranas',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Membranas', choices=[('C', 'Completa'), ('I', 'Incompleta')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='placenta',
            name='placenta_desprendimiento',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Desprendimiento', choices=[('C', 'Completa'), ('I', 'Incompleta')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='placenta',
            name='placenta_peso',
            field=models.IntegerField(blank=True, null=True, verbose_name='Peso', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='placenta',
            name='placenta_tamanio_ancho',
            field=models.IntegerField(blank=True, null=True, verbose_name='Ancho', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='placenta',
            name='placenta_tamanio_longitud',
            field=models.IntegerField(blank=True, null=True, verbose_name='Longitud', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='placenta',
            name='placenta_tipo',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Tipo', choices=[('shultz', 'Shultz'), ('duncan', 'Duncan')]),
            preserve_default=True,
        ),
    ]
