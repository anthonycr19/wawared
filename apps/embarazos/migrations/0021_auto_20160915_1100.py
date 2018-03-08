# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0020_auto_20160713_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planparto',
            name='donador_1_edad',
            field=models.CharField(blank=True, max_length=2, null=True, validators=[django.core.validators.RegexValidator(regex=b'[0-9]{1,2}$', message='La edad solo debe contener d\xedgitos')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='planparto',
            name='donador_2_edad',
            field=models.CharField(blank=True, max_length=2, null=True, validators=[django.core.validators.RegexValidator(regex=b'[0-9]{1,2}$', message='La edad solo debe contener d\xedgitos')]),
            preserve_default=True,
        ),
    ]
