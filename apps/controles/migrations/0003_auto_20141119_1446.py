# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0002_auto_20141102_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='ic_medicina',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='ic_nutricion',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='ic_odontologia',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='ic_psicologia',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
