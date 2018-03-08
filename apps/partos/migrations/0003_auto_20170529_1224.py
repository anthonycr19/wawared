# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partos', '0002_auto_20170502_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partogramamedicion',
            name='moldeaminetos',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Moldeamientos', choices=[('1', '1'), ('2', '2'), ('3', '3')]),
            preserve_default=True,
        ),
    ]
