# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, transaction
import django.core.validators

def change_altura_presentacion_values(apps, schema_editor):
    examenes = apps.get_model('controles', 'ExamenFisico')
    for examen in examenes.objects.all():
        if examen.tv_altura_presentacion is not None:
            examen.tv_altura_presentacion = str(abs(int(examen.tv_altura_presentacion)-5))
            examen.save()

class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0043_auto_20171013_1251'),
    ]

    operations = [
        migrations.RunPython(change_altura_presentacion_values)
    ]
