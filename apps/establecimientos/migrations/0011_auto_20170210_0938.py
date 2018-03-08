# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0010_establecimiento_is_sistema_externo_admision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establecimiento',
            name='nombre',
            field=models.CharField(max_length=150, verbose_name='Nombre'),
            preserve_default=True,
        ),
    ]
