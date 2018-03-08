# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partogramamedicion',
            name='tv_incorporacion',
            field=models.CharField(blank=True, max_length=20, verbose_name='Incorporaci\xf3n', choices=[('-40%', 'menos de 40%'), ('50%', '50%'), ('70%', '70%'), ('80%', '80%'), ('90%', '90%'), ('100%', '100%')]),
            preserve_default=True,
        ),
    ]
