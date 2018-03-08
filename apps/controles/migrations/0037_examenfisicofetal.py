# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0036_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamenFisicoFetal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fcf', models.SmallIntegerField(max_length=3, null=True, verbose_name='FCF', blank=True)),
                ('situacion', models.CharField(blank=True, max_length=20, null=True, verbose_name='Situacion', choices=[('l', 'Longitudinal'), ('t', 'Transversal'), ('na', 'Indiferente')])),
                ('presentacion', models.CharField(blank=True, max_length=20, null=True, verbose_name='Presentacion', choices=[('c', 'Cefalico'), ('p', 'Podalico'), ('na', 'Indiferente')])),
                ('posicion', models.CharField(blank=True, max_length=20, null=True, verbose_name='Posicion', choices=[('d', 'Derecho'), ('i', 'Izquierdo'), ('na', 'Indiferente')])),
                ('movimientos_fetales', models.CharField(blank=True, max_length=5, null=True, verbose_name='Movimientos fetales', choices=[('sm', 'Sin Movimiento'), ('+', '+'), ('++', '++'), ('+++', '+++'), ('na', 'NA')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('control', models.ForeignKey(related_name='control', to='controles.Control')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
