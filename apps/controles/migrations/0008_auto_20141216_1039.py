# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0007_auto_20141216_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examenfisico',
            name='tv_membranas_rotas_tipo',
            field=models.CharField(blank=True, max_length=10, verbose_name='', choices=[('artificial', 'Artificial'), ('espontanea', 'Espontanea')]),
            preserve_default=True,
        ),
    ]
