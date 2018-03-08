# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='control',
            field=models.ForeignKey(related_name='citas', blank=True, to='controles.Control', null=True),
            preserve_default=True,
        ),
    ]
