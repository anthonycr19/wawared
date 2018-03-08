# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0023_planparto_telefono'),
    ]

    operations = [
        migrations.AddField(
            model_name='bebe',
            name='no_recuerda_fecha',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
