# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0024_auto_20160507_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacuna',
            name='influenza',
            field=models.NullBooleanField(verbose_name=b'Influenza'),
            preserve_default=True,
        ),
    ]
