# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0003_auto_20141119_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='ic_enfermeria',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
