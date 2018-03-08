# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0002_auto_20141107_0944'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Usuario de sistema', 'verbose_name_plural': 'Usuarios del sistema'},
        ),
        migrations.AlterModelOptions(
            name='usuarioestablecimiento',
            options={'verbose_name': 'Usuario Establecimiento', 'verbose_name_plural': 'Usuarios de Establecimiento'},
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(default='observador', max_length=100, verbose_name='Tipo de usuario', choices=[('medico', 'Medico'), ('licenciado', 'Obstetra'), ('observador', 'Observador'), ('capacitacion', 'Capacitaci\xf3n')]),
            preserve_default=True,
        ),
    ]
