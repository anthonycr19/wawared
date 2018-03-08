# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServicioReniec',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('namespace', models.CharField(max_length=250, verbose_name=b'NameSpace')),
                ('urlwsdlservice', models.CharField(max_length=500, verbose_name=b'UrlWSLD')),
                ('appservice', models.CharField(max_length=100, verbose_name=b'App')),
                ('userservice', models.CharField(max_length=8, verbose_name=b'User')),
                ('passservice', models.CharField(max_length=500, verbose_name=b'Password')),
            ],
            options={
                'verbose_name': 'SERVICIO DNI RENIEC',
                'verbose_name_plural': 'SERVICIO DNI RENIECS',
            },
            bases=(models.Model,),
        ),
    ]
