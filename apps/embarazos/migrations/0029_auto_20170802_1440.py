# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0028_auto_20170502_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='embarazo',
            name='talla',
            field=models.FloatField(verbose_name='Talla'),
            preserve_default=True,
        ),
    ]
