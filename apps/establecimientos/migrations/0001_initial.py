# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diresa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Establecimiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=50, verbose_name='C\xf3digo')),
                ('disa', models.CharField(max_length=50, null=True, verbose_name=b'Disa', blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'establecimientos/logos/')),
                ('telefono', models.CharField(max_length=20, verbose_name='Tel\xe9fono', blank=True)),
                ('nombre', models.CharField(unique=True, max_length=150, verbose_name='Nombre')),
                ('descripcion', models.TextField(max_length=150, null=True, verbose_name='Descripci\xf3n', blank=True)),
                ('codigo_his', models.CharField(max_length=10, verbose_name='C\xf3digo HIS')),
                ('lote', models.SmallIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('diresa', models.ForeignKey(blank=True, editable=False, to='establecimientos.Diresa', null=True)),
            ],
            options={
                'verbose_name': 'Establecimiento',
                'verbose_name_plural': 'Establecimientos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Microred',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Micro Red',
                'verbose_name_plural': 'Micro Redes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Red',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('diresa', models.ForeignKey(blank=True, to='establecimientos.Diresa', null=True)),
            ],
            options={
                'verbose_name': 'Red',
                'verbose_name_plural': 'Redes',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='microred',
            name='red',
            field=models.ForeignKey(blank=True, to='establecimientos.Red', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='establecimiento',
            name='microred',
            field=models.ForeignKey(blank=True, to='establecimientos.Microred', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='establecimiento',
            name='red',
            field=models.ForeignKey(blank=True, to='establecimientos.Red', null=True),
            preserve_default=True,
        ),
    ]
