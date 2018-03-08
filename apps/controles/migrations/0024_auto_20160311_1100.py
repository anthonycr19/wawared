# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0023_auto_20160310_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control',
            name='zika_viajo',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('no', 'No'), ('si', 'Si')]),
            preserve_default=True,
        ),
    ]
