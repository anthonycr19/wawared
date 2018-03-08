# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partos', '0007_auto_20171109_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='placenta',
            name='liquido_amniotico_otras_caracteristicas',
            field=models.TextField(null=True, verbose_name='Otras caracter\xedsticas', blank=True),
            preserve_default=True,
        ),
    ]
