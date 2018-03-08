# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0003_auto_20150126_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='microred',
            name='numero',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
