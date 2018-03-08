# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0032_auto_20160915_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='synchronize',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
