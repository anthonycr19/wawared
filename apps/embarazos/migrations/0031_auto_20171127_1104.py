# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0030_auto_20170926_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planparto',
            name='observaciones',
        ),
        migrations.AddField(
            model_name='planparto',
            name='dolor_cabeza_abdominal',
            field=models.BooleanField(default=False, verbose_name='Dolor de cabeza y dolor abdominal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='fiebre_escalofrios',
            field=models.BooleanField(default=False, verbose_name='Fiebre o escalofr\xedos'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='hinchazon',
            field=models.BooleanField(default=False, verbose_name='Hinchaz\xf3n de cara , manos y pies'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='salida_vagina',
            field=models.BooleanField(default=False, verbose_name='Salida de sangre o liquido por su vagina'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='vomito_exagerado',
            field=models.BooleanField(default=False, verbose_name='V\xf3mito exagerado'),
            preserve_default=True,
        ),
    ]
