# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0003_auto_20141107_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(default='observador', max_length=100, verbose_name='Tipo de usuario', choices=[('medico', 'Medico'), ('licenciado', 'Obstetra'), ('observador', 'Observador'), ('estadistica', 'Estad\xedstica')]),
            preserve_default=True,
        ),
    ]
