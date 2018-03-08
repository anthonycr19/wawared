# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0026_auto_20160513_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control',
            name='proteinuria_cualitativa',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='proteurina cualitativa', choices=[('-', 'negativo'), ('+', '+'), ('++', '++'), ('+++', '+++'), ('nsh', 'No Se Hizo')]),
            preserve_default=True,
        ),
    ]
