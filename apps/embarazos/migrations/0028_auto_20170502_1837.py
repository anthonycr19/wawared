# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0027_remove_ecografiadetalle_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecografia',
            name='fecha',
            field=models.DateField(null=True, verbose_name='Fecha de la ecograf\xeda'),
            preserve_default=True,
        ),
    ]
