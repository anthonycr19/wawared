# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0002_auto_20150126_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='fecha_asistio',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
