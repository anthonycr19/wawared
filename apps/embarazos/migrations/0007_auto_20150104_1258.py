# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0006_auto_20150104_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='fichaviolenciafamiliar',
            name='cefalea',
            field=models.NullBooleanField(default=None, verbose_name='Cefalea problemas de sue\xf1o (mucho sue\xf1o, interrupci\xf3n del sue\xf1o)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaviolenciafamiliar',
            name='quejas_cronicas',
            field=models.NullBooleanField(default=None, verbose_name='Quejas cr\xf3nicas sin causa f\xedsica'),
            preserve_default=True,
        ),
    ]
