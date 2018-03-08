# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0008_auto_20150406_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='codigo',
            field=models.CharField(max_length=20, null=True, editable=False),
            preserve_default=True,
        ),
    ]
