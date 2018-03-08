# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0002_auto_20141102_2340'),
        ('pacientes', '0001_initial'),
        ('establecimientos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('origen', models.CharField(default=b'interno', max_length=10, choices=[(b'interno', b'Interno'), (b'externo', b'Externo')])),
                ('asistio', models.NullBooleanField(default=None, verbose_name=b'Asistio')),
                ('tipo', models.CharField(max_length=10, verbose_name=b'Tipo de cita', choices=[(b'control', b'Tipo Control'), (b'gestacion', b'Tipo gestaci\xc3\xb3n')])),
                ('fecha', models.DateTimeField()),
                ('is_wawared', models.BooleanField(default=False, verbose_name=b'Es Wawared')),
                ('comentario', models.TextField(null=True, verbose_name=b'Comentario', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('control', models.ForeignKey(related_name='ciitas', blank=True, to='controles.Control', null=True)),
                ('establecimiento', models.ForeignKey(related_name='citas', to='establecimientos.Establecimiento')),
                ('paciente', models.ForeignKey(related_name='citas', to='pacientes.Paciente')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='cita',
            unique_together=set([('fecha', 'establecimiento')]),
        ),
    ]
