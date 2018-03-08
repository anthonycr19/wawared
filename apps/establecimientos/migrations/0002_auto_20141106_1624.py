# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establecimiento',
            name='codigo_his',
            field=models.CharField(max_length=10, null=True, verbose_name='C\xf3digo HIS', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'establecimientos/logos/', blank=True),
            preserve_default=True,
        ),
    ]
