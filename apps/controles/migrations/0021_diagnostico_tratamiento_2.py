# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0020_auto_20150708_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnostico',
            name='tratamiento_2',
            field=models.TextField(null=True, verbose_name='Tratamiento 2', blank=True),
            preserve_default=True,
        ),
    ]
