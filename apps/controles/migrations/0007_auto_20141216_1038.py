# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0006_auto_20141205_1123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examenfisico',
            name='tv_liquido_anmiotico',
        ),
        migrations.AddField(
            model_name='examenfisico',
            name='tv_altura_presentacion',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Altura de presentaci\xf3n', choices=[(-4, b'-4'), (-3, b'-3'), (-2, b'-2'), (-1, b'-1'), (0, b'0'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='examenfisico',
            name='tv_dilatacion',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Dilataci\xf3n', choices=[(0, b'0'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9'), (10, b'10')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='examenfisico',
            name='tv_liquido_amniotico',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='L\xedquido amni\xf3tico', choices=[('claro', 'Claro'), ('meconial', 'Meconial'), ('sanguinolento', 'Sanguinolento')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='examenfisico',
            name='tv_membranas_rotas_tipo',
            field=models.CharField(default='', max_length=10, blank=True, choices=[('artificial', 'Artificial'), ('espontanea', 'Espontanea')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='examenfisico',
            name='tv_incorporacion',
            field=models.CharField(blank=True, max_length=20, verbose_name='Incorporaci\xf3n', choices=[('-40%', 'menos de 40%'), ('50%', '50%'), ('70%', '70%'), ('80%', '80%'), ('90%', '90%')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='examenfisico',
            name='tv_membranas',
            field=models.CharField(blank=True, max_length=10, verbose_name='Membranas', choices=[('integras', '\xcdntegras'), ('rotas', 'Rotas')]),
            preserve_default=True,
        ),
    ]
