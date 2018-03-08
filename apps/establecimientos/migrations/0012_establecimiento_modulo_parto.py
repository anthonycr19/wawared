# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0011_auto_20170210_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='establecimiento',
            name='modulo_parto',
            field=models.BooleanField(default=False, verbose_name='Parto'),
            preserve_default=True,
        ),
    ]
