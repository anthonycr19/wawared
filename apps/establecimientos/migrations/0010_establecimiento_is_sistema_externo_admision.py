# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0009_auto_20160705_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='establecimiento',
            name='is_sistema_externo_admision',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
