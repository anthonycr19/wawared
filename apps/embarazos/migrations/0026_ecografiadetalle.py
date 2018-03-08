# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('embarazos', '0025_auto_20170418_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='EcografiaDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('biometria_fetal', models.PositiveSmallIntegerField(null=True, verbose_name='Biometr\xeda Fetal (Per\xedmetro cef\xe1lico)', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
                ('ecografia', models.ForeignKey(related_name='ecografia', to='embarazos.Ecografia')),
            ],
            options={
                'verbose_name': 'Ecografia Detalle',
                'verbose_name_plural': 'Ecografias Detalles',
            },
            bases=(models.Model,),
        ),
    ]
