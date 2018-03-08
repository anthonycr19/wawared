# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0017_auto_20150407_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examenfisico',
            name='tv_altura_presentacion',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Altura de presentaci\xf3n', choices=[('0', '0 || -4'), ('1', '1 || -3'), ('2', '2 || -2'), ('3', '3 || -1/0'), ('4', '4 || +1/+2'), ('5', '5 || +3/+4')]),
            preserve_default=True,
        ),
    ]
