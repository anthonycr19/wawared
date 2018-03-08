# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0014_auto_20170825_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establecimiento',
            name='fuas_incremento',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='fuas_numfinal',
            field=models.IntegerField(default=0, verbose_name=b'NUmero de FUA rango Final SIS'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='fuas_numinicial',
            field=models.IntegerField(default=0, verbose_name=b'Numero de FUA rango inicial SIS'),
            preserve_default=True,
        ),
    ]
