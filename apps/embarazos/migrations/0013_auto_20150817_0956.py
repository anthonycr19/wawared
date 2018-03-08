# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    def copy_father_name(apps, schema_editor):
        Embarazo = apps.get_model('embarazos', 'Embarazo')
        for embarazo in Embarazo.objects.all():
            embarazo.padre_apellido_paterno = embarazo.padre
            embarazo.padre_apellido_materno = embarazo.padre
            embarazo.padre_nombres = embarazo.padre
            embarazo.save()

    dependencies = [
        ('embarazos', '0012_auto_20150817_0955'),
    ]

    operations = [
        migrations.RunPython(copy_father_name)
    ]
