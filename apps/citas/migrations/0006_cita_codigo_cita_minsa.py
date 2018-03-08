# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0005_auto_20170111_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='codigo_cita_minsa',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
    ]
