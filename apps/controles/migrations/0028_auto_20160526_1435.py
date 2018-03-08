# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0027_auto_20160518_1147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examenfisico',
            old_name='especuloscopia_cervix',
            new_name='especuloscopia_cervix_observaciones',
        ),
        migrations.RenameField(
            model_name='examenfisico',
            old_name='especuloscopia_fondo_de_saco',
            new_name='especuloscopia_fondo_de_saco_observaciones',
        ),
        migrations.RenameField(
            model_name='examenfisico',
            old_name='especuloscopia_vagina',
            new_name='especuloscopia_vagina_observaciones',
        ),
    ]
