# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0046_auto_20171113_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='oc_signos_alarma',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
