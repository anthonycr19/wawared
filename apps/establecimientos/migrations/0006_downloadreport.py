# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('establecimientos', '0005_auto_20150309_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'', null=True, verbose_name=b'reports/%Y/%m/%d/', blank=True)),
                ('filename', models.CharField(max_length=100)),
                ('content_type', models.CharField(max_length=100)),
                ('status', models.CharField(default=b'in process', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(related_name='download_report', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
