# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0004_control_ic_enfermeria'),
    ]

    operations = [
        migrations.AddField(
            model_name='examenfisico',
            name='especuloscopia',
            field=models.BooleanField(default=False, verbose_name='Especuloscop\xeda'),
            preserve_default=True,
        ),
    ]
