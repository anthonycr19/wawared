# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0018_auto_20150409_1251'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='diagnosticodetalle',
            options={'ordering': ('order', 'cie__nombre')},
        ),
        migrations.AddField(
            model_name='diagnosticodetalle',
            name='order',
            field=models.SmallIntegerField(default=0, verbose_name='Orden'),
            preserve_default=True,
        ),
    ]
