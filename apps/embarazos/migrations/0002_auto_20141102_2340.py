# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cie', '0001_initial'),
        ('embarazos', '0001_initial'),
        ('pacientes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ultimoembarazo',
            name='created_by',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ultimoembarazo',
            name='embarazo',
            field=models.ForeignKey(to='embarazos.Embarazo', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ultimoembarazo',
            name='establecimiento',
            field=models.ForeignKey(related_name='ultimos_embarazos', to='establecimientos.Establecimiento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ultimoembarazo',
            name='paciente',
            field=models.ForeignKey(related_name='ultimos_embarazos', to='pacientes.Paciente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='created_by',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='embarazo',
            field=models.OneToOneField(related_name='plan_parto', to='embarazos.Embarazo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='establecimiento',
            field=models.ForeignKey(related_name='planes_parto', to='establecimientos.Establecimiento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fichaviolenciafamiliar',
            name='created_by',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fichaviolenciafamiliar',
            name='embarazo',
            field=models.OneToOneField(related_name='ficha_violencia_familiar', to='embarazos.Embarazo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fichaviolenciafamiliar',
            name='paciente',
            field=models.ForeignKey(related_name='fichas_violencia_familiar', to='pacientes.Paciente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fichaproblema',
            name='created_by',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fichaproblema',
            name='embarazo',
            field=models.OneToOneField(related_name='ficha_problema', to='embarazos.Embarazo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fichaproblema',
            name='paciente',
            field=models.ForeignKey(related_name='fichas_problema', to='pacientes.Paciente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='embarazo',
            name='created_by',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='embarazo',
            name='emergencia_diagnosticos',
            field=models.ManyToManyField(related_name='embarazos_emergencias', null=True, to='cie.ICD10Base', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='embarazo',
            name='establecimiento',
            field=models.ForeignKey(related_name='embarazos', to='establecimientos.Establecimiento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='embarazo',
            name='hospitalizacion_diagnosticos',
            field=models.ManyToManyField(related_name='embarazos_hospitalizacion', null=True, to='cie.ICD10Base', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='embarazo',
            name='paciente',
            field=models.ForeignKey(related_name='embarazos', to='pacientes.Paciente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ecografia',
            name='created_by',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ecografia',
            name='embarazo',
            field=models.ForeignKey(related_name='ecografias', to='embarazos.Embarazo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ecografia',
            name='establecimiento',
            field=models.ForeignKey(related_name='ecografias', to='establecimientos.Establecimiento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bebe',
            name='embarazo',
            field=models.ForeignKey(related_name='bebes', to='embarazos.UltimoEmbarazo'),
            preserve_default=True,
        ),
    ]
