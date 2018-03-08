# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0019_auto_20150526_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control',
            name='eg_elegida',
            field=models.CharField(default='fum', max_length=20, verbose_name='EG escogida', blank=True, choices=[('fum', 'FUM'), ('ecografia', 'Ecograf\xeda'), ('altura uterina', 'Altura Uterina')]),
            preserve_default=True,
        ),
    ]
