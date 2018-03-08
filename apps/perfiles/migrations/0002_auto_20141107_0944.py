# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='colegiatura',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name=b'Colegiatura', validators=[django.core.validators.RegexValidator(regex=b'^\\d+$', message='Se deben ingresar valores num\xe9ricos')]),
            preserve_default=True,
        ),
    ]
