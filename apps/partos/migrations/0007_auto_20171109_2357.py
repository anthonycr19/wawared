# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, transaction
import django.core.validators

def change_decenso_cefalico_values(apps, schema_editor):
    mediciones = apps.get_model('partos', 'PartogramaMedicion')
    for medicion in mediciones.objects.all():
        if medicion.tv_descenso_cefalico is not None:
            medicion.tv_descenso_cefalico = str(abs(int(medicion.tv_descenso_cefalico)-5))
            medicion.save()

class Migration(migrations.Migration):

    dependencies = [
        ('partos', '0006_auto_20171026_1500'),
    ]

    operations = [
        migrations.RunPython(change_decenso_cefalico_values)
    ]
