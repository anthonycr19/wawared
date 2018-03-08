# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0012_auto_20160620_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='celular',
            field=models.CharField(max_length=15, null=True, verbose_name='Celular', blank=True),
            preserve_default=True,
        ),
    ]
