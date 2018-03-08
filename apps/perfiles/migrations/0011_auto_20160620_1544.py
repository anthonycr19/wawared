# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0010_user_celular'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='his',
            field=models.CharField(max_length=13, null=True, verbose_name='HIS', blank=True),
            preserve_default=True,
        ),
    ]
