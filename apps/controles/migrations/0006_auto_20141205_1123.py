# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0005_examenfisico_especuloscopia'),
    ]

    operations = [
        migrations.AddField(
            model_name='examenfisico',
            name='examen_ginecologico',
            field=models.NullBooleanField(default=None, verbose_name='Examen ginecol\xf3gico'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='examenfisico',
            name='especuloscopia',
            field=models.NullBooleanField(default=None, verbose_name='Especuloscop\xeda'),
            preserve_default=True,
        ),
    ]
