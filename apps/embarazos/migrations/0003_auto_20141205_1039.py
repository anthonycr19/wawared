# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0002_auto_20141102_2340'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ecografia',
            options={'ordering': ('fecha',), 'verbose_name': 'Ecografia', 'verbose_name_plural': 'Ecografias'},
        ),
        migrations.AddField(
            model_name='ecografia',
            name='tipo_embarazo',
            field=models.CharField(default=b'unico', max_length=10, verbose_name=b'Tipo de embarazo', choices=[(b'unico', '\xdanico'), (b'multiple', b'Multiple')]),
            preserve_default=True,
        ),
    ]
