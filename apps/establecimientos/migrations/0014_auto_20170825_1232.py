# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0013_establecimiento_modulo_citas'),
    ]

    operations = [
        migrations.AddField(
            model_name='establecimiento',
            name='fuas_categoria',
            field=models.CharField(max_length=2, null=True, verbose_name=b'Categoria SIS', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='establecimiento',
            name='fuas_codconvenido',
            field=models.CharField(max_length=1, null=True, verbose_name=b'Codigo Convenio SIS', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='establecimiento',
            name='fuas_disa',
            field=models.CharField(max_length=3, null=True, verbose_name=b'DISA SIS', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='establecimiento',
            name='fuas_incremento',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='establecimiento',
            name='fuas_nivel',
            field=models.CharField(max_length=1, null=True, verbose_name=b'Nivel SIS', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='establecimiento',
            name='fuas_numfinal',
            field=models.SmallIntegerField(default=0, verbose_name=b'NUmero de FUA rango Final SIS'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='establecimiento',
            name='fuas_numinicial',
            field=models.SmallIntegerField(default=0, verbose_name=b'Numero de FUA rango inicial SIS'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='establecimiento',
            name='fuas_trama',
            field=models.NullBooleanField(verbose_name=b'Habilitada Trma SIS'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='establecimiento',
            name='fuas_udr',
            field=models.CharField(max_length=3, null=True, verbose_name=b'UDR SIS', blank=True),
            preserve_default=True,
        ),
    ]
