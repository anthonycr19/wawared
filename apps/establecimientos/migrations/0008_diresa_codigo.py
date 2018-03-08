# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0007_auto_20150317_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='diresa',
            name='codigo',
            field=models.CharField(max_length=3, null=True, blank=True),
            preserve_default=True,
        ),
    ]
