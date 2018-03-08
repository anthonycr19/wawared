# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ubigeo', '0001_initial'),
        ('controles', '0022_auto_20160307_1654'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='control',
            options={'ordering': ['numero'], 'verbose_name': 'Atenci\xf3n', 'verbose_name_plural': 'Atenciones'},
        ),
        migrations.AddField(
            model_name='control',
            name='zika_departamento',
            field=models.ForeignKey(related_name='zina_departamento', blank=True, to='ubigeo.Departamento', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='zika_pais',
            field=models.ForeignKey(related_name='zika_pais', blank=True, to='ubigeo.Pais', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='zika_provincia',
            field=models.ForeignKey(related_name='zina_provincia', blank=True, to='ubigeo.Provincia', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='zika_sintoma_conjuntivitis',
            field=models.BooleanField(default=False, verbose_name='Conjuntivitis'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='zika_sintoma_dolorcabeza',
            field=models.BooleanField(default=False, verbose_name='Dolor de cabeza'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='zika_sintoma_fiebre',
            field=models.BooleanField(default=False, verbose_name='Fiebre'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='zika_sintoma_malestar',
            field=models.BooleanField(default=False, verbose_name='Malestar General'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='zika_sintoma_sarpullido',
            field=models.BooleanField(default=False, verbose_name='Sarpullido'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='zika_viajo',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
