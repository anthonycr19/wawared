# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0022_auto_20170119_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='planparto',
            name='telefono',
            field=models.IntegerField(null=True, verbose_name='Tel\xe9fono', blank=True),
            preserve_default=True,
        ),
    ]
