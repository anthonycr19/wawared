# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0006_downloadreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='downloadreport',
            name='file',
            field=models.FileField(null=True, upload_to=b'reports/%Y/%m/%d/', blank=True),
            preserve_default=True,
        ),
    ]
