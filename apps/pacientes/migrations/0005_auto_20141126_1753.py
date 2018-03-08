# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0004_auto_20141103_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='foto',
            field=models.ImageField(upload_to=b'fotos/%Y/%m/%d/', null=True, verbose_name='Foto', blank=True),
            preserve_default=True,
        ),
    ]
