# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0004_microred_numero'),
    ]

    operations = [
        migrations.AddField(
            model_name='diresa',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'diresas/logos/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='red',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'redes/logos/', blank=True),
            preserve_default=True,
        ),
    ]
