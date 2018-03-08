# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0026_ecografiadetalle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ecografiadetalle',
            name='created_by',
        ),
    ]
