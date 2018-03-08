# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0007_auto_20170523_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='is_confirmado_cita_minsa',
            field=models.NullBooleanField(default=None),
            preserve_default=True,
        ),
    ]
