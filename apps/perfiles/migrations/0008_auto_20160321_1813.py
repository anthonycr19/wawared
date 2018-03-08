# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0007_user_servicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(default='observador', max_length=100, verbose_name='Tipo de usuario', choices=[('medico', 'M\xe9dico'), ('licenciado', 'Obstetra'), ('observador', 'Observador'), ('estadistica', 'Estad\xedstica'), ('gestante', 'Gestante')]),
            preserve_default=True,
        ),
    ]
