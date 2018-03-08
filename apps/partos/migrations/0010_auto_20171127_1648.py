# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partos', '0009_auto_20171122_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminacionembarazo',
            name='fecha_referido',
            field=models.DateField(null=True, verbose_name='Fecha Referido', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='referido',
            field=models.CharField(default='n', max_length=1, verbose_name='\xbfEs referida?', choices=[('s', 'Si'), ('n', 'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='terminacionembarazo',
            name='fecha',
            field=models.DateField(default=None, null=True, verbose_name='Fecha', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='terminacionembarazo',
            name='hora',
            field=models.TimeField(default=None, null=True, verbose_name='Hora', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='terminacionembarazo',
            name='tipo',
            field=models.CharField(default='unico', max_length=20, null=True, blank=True, choices=[('unico', '\xdanico'), ('multiple', 'M\xfaltiple')]),
            preserve_default=True,
        ),
    ]
