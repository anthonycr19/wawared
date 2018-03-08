# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0029_auto_20160526_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control',
            name='altura_uterina',
            field=models.SmallIntegerField(null=True, verbose_name='Altura uterina', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='control',
            name='fcf',
            field=models.SmallIntegerField(max_length=3, null=True, verbose_name='FCF', blank=True),
            preserve_default=True,
        ),
    ]
