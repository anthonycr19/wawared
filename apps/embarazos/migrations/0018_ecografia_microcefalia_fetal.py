# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0017_auto_20160621_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecografia',
            name='microcefalia_fetal',
            field=models.CharField(blank=True, max_length=2, choices=[(b'si', b'Si'), (b'no', b'No')]),
            preserve_default=True,
        ),
    ]
