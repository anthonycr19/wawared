# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0028_auto_20160526_1435'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examenfisico',
            old_name='especuloscopia_cervix_observaciones',
            new_name='especuloscopia_cervix',
        ),
        migrations.RenameField(
            model_name='examenfisico',
            old_name='especuloscopia_fondo_de_saco_observaciones',
            new_name='especuloscopia_fondo_de_saco',
        ),
        migrations.RenameField(
            model_name='examenfisico',
            old_name='especuloscopia_vagina_observaciones',
            new_name='especuloscopia_vagina',
        ),
    ]
