# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cpt', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('controles', '0033_control_synchronize'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcedimientoDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('observacion', models.CharField(max_length=200, null=True, blank=True)),
                ('order', models.SmallIntegerField(default=0, verbose_name='Orden')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('cpt', models.ForeignKey(to='cpt.CatalogoProcedimiento', null=True)),
                ('created_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
                ('diagnostico', models.ForeignKey(related_name='procedimientos', to='controles.Diagnostico')),
            ],
            options={
                'ordering': ('order', 'cpt__denominacion_procedimientos'),
            },
            bases=(models.Model,),
        ),
    ]
