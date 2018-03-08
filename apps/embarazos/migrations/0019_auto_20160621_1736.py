# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0018_ecografia_microcefalia_fetal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecografia',
            name='microcefalia_fetal',
            field=models.CharField(blank=True, max_length=2, verbose_name='Informe con probable microcefalia fetal/calcificaci\xf3n intracraneal', choices=[(b'si', b'Si'), (b'no', b'No')]),
            preserve_default=True,
        ),
    ]
