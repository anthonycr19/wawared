# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0013_auto_20150817_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='embarazo',
            name='fecha_tamizaje',
            field=models.DateField(null=True, verbose_name=b'Fecha de tamizaje', blank=True),
            preserve_default=True,
        ),
    ]
