# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, transaction
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0042_auto_20170920_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examenfisico',
            name='tv_altura_presentacion',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Altura de presentaci\xf3n', choices=[('5', '5/5'), ('4', '4/5'), ('3', '3/5'), ('2', '2/5'), ('1', '1/5'), ('0', '0/5')]),
            preserve_default=True,
        ),
    ]
