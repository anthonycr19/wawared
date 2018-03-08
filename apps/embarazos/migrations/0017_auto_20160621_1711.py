# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0016_auto_20160317_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecografia',
            name='biometria_fetal',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Biometr\xeda Fetal (Per\xedmetro cef\xe1lico)', blank=True),
            preserve_default=True,
        ),
    ]
