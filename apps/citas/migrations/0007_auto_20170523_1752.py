# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0006_cita_codigo_cita_minsa'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cita',
            old_name='codigo_cita_minsa',
            new_name='uuid_cita_minsa',
        ),
    ]
