# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0001_initial'),
        ('establecimientos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('embarazos', '0001_initial'),
        ('pacientes', '0001_initial'),
        ('cie', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sintoma',
            name='created_by',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='control',
            field=models.OneToOneField(related_name='laboratorio', to='controles.Control'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='created_by',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='examenlaboratorio',
            name='created_by',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='examenfisico',
            name='control',
            field=models.OneToOneField(related_name='examen_fisico', to='controles.Control'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='examenfisico',
            name='created_by',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diagnosticodetalle',
            name='cie',
            field=models.ForeignKey(to='cie.ICD10'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diagnosticodetalle',
            name='created_by',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diagnosticodetalle',
            name='diagnostico',
            field=models.ForeignKey(related_name='detalles', to='controles.Diagnostico'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diagnostico',
            name='control',
            field=models.OneToOneField(related_name='diagnostico', to='controles.Control'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diagnostico',
            name='created_by',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diagnostico',
            name='otros_examenes',
            field=models.ManyToManyField(related_name='diagnosticos', to='controles.ExamenLaboratorio', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diagnostico',
            name='paciente',
            field=models.ForeignKey(related_name='diagnosticos', to='pacientes.Paciente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='created_by',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='embarazo',
            field=models.ForeignKey(related_name='controles', to='embarazos.Embarazo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='establecimiento',
            field=models.ForeignKey(related_name='controles', to='establecimientos.Establecimiento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='paciente',
            field=models.ForeignKey(related_name='controles', to='pacientes.Paciente'),
            preserve_default=True,
        ),
    ]
