# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=6, verbose_name=b'Codigo', blank=True)),
                ('nombre', models.CharField(max_length=100, verbose_name=b'Nombre')),
            ],
            options={
                'verbose_name': 'Departameto',
                'verbose_name_plural': 'Departamentos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Distrito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=6, verbose_name=b'Codigo', blank=True)),
                ('nombre', models.CharField(max_length=100, verbose_name=b'Nombre')),
            ],
            options={
                'verbose_name': 'Distrito',
                'verbose_name_plural': 'Distritos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=3, verbose_name=b'Codigo')),
                ('nombre', models.CharField(max_length=100, verbose_name=b'Nombre')),
            ],
            options={
                'verbose_name': 'Pa\xeds',
                'verbose_name_plural': 'Paises',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=6, verbose_name=b'Codigo', blank=True)),
                ('nombre', models.CharField(max_length=100, verbose_name=b'Nombre')),
                ('departamento', models.ForeignKey(verbose_name=b'Departamento', to='ubigeo.Departamento')),
            ],
            options={
                'verbose_name': 'Provincia',
                'verbose_name_plural': 'Provincias',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='distrito',
            name='provincia',
            field=models.ForeignKey(verbose_name=b'Provincia', to='ubigeo.Provincia'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='departamento',
            name='pais',
            field=models.ForeignKey(verbose_name=b'Pais', to='ubigeo.Pais'),
            preserve_default=True,
        ),
    ]
