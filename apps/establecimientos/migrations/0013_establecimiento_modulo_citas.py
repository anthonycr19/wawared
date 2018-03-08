# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0012_establecimiento_modulo_parto'),
    ]

    operations = [
        migrations.AddField(
            model_name='establecimiento',
            name='modulo_citas',
            field=models.BooleanField(default=False, verbose_name='Citas'),
            preserve_default=True,
        ),
    ]
