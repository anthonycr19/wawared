# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0037_examenfisicofetal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboratorio',
            name='factor',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Factor RH', choices=[('+', '+'), ('-', '-'), ('- sen desc', '- Sen Desc'), ('- no sen', '- No Sen'), ('- sen', '- Sen')]),
            preserve_default=True,
        ),
    ]
