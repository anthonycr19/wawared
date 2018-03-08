# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0006_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='servicio',
            field=models.CharField(max_length=20, null=True, verbose_name='Servicio', blank=True),
            preserve_default=True,
        ),
    ]
