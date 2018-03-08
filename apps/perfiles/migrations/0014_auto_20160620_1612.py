# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0013_auto_20160620_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dni',
            field=models.CharField(max_length=8, null=True, verbose_name='DNI', blank=True),
            preserve_default=True,
        ),
    ]
