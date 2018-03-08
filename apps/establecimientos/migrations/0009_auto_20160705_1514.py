# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0008_diresa_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establecimiento',
            name='codigo',
            field=models.CharField(max_length=50, verbose_name='C\xf3digo Renaes'),
            preserve_default=True,
        ),
    ]
