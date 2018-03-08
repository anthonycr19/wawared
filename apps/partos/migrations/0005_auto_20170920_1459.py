# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('partos', '0004_auto_20170915_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecienNacido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sexo', models.CharField(default='M', max_length=1, null=True, verbose_name='Sexo', choices=[('M', 'Masculino'), ('F', 'Femenino')])),
                ('peso', models.DecimalField(decimal_places=1, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)], null=True, verbose_name='Peso')),
                ('talla', models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(240)], null=True, verbose_name='Talla')),
                ('apgar_1', models.CharField(default=0, max_length=2, null=True, verbose_name='APGAR 1\xb0', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])),
                ('apgar_5', models.CharField(default=0, max_length=2, null=True, verbose_name='APGAR 5\xb0', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])),
                ('terminacion_embarazo', models.ForeignKey(blank=True, to='partos.TerminacionEmbarazo', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='ingreso',
            name='fcf',
        ),
    ]
