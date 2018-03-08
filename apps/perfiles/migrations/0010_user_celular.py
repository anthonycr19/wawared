# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0009_user_contrasena_gestante'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='celular',
            field=models.CharField(blank=True, max_length=9, null=True, verbose_name='Celular', validators=[django.core.validators.RegexValidator(regex='^\\d{9}$', message='El n\xfamero de DNI debe contener 9 d\xedgitos')]),
            preserve_default=True,
        ),
    ]
