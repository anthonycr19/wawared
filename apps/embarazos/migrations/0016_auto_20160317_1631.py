# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0015_auto_20151214_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecografia',
            name='biometria_fetal',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Biometr\xeda Fetal', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ecografia',
            name='ila',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='\xcdndice de l\xedquido amni\xf3tico', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ecografia',
            name='liquido_amniotico',
            field=models.CharField(default='', max_length=1, blank=True, choices=[(b'n', b'Normal'), (b'd', b'Disminuido'), (b'a', b'Aumentado')]),
            preserve_default=False,
        ),
    ]
