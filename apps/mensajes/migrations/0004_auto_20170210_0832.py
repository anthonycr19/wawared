# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('mensajes', '0003_auto_20170206_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensajes',
            name='mensaje',
            field=models.CharField(max_length=200, verbose_name='Mensaje', validators=[django.core.validators.RegexValidator(regex="^[0-9a-zA-Z\xe0\xe1\xe2\xe4\xe3\xe5\u0105\u010d\u0107\u0119\xe8\xe9\xea\xeb\u0117\u012f\xec\xed\xee\xef\u0142\u0144\xf2\xf3\xf4\xf6\xf5\xf8\xf9\xfa\xfb\xfc\u0173\u016b\xff\xfd\u017c\u017a\xf1\xe7\u010d\u0161\u017e\xc0\xc1\xc2\xc4\xc3\xc5\u0104\u0106\u010c\u0116\u0118\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\u012e\u0141\u0143\xd2\xd3\xd4\xd6\xd5\xd8\xd9\xda\xdb\xdc\u0172\u016a\u0178\xdd\u017b\u0179\xd1\xdf\xc7\u0152\xc6\u010c\u0160\u017d\u2202\xf0 ,.\\'-]+$", message='Solo caracteres validos')]),
            preserve_default=True,
        ),
    ]
