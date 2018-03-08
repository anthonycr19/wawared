# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('perfiles', '0016_auto_20160620_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupRolMinsa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo_rol_minsa', models.CharField(max_length=3, verbose_name='Rol Minsa login')),
                ('group', models.ForeignKey(verbose_name='Grupo del Sistema', to='auth.Group')),
            ],
            options={
                'verbose_name': 'Grupo_Roles_Minsa',
                'verbose_name_plural': 'Grupos_Roles_Minsa',
            },
            bases=(models.Model,),
        ),
    ]
