# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0008_auto_20160321_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contrasena_gestante',
            field=models.CharField(default='', max_length=5, editable=False, blank=True),
            preserve_default=False,
        ),
    ]
