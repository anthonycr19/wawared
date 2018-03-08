# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0015_auto_20170829_0855'),
        ('partos', '0008_placenta_liquido_amniotico_otras_caracteristicas'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pacientes', '0032_auto_20170410_1621'),
        ('puerperio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TerminacionPuerpera',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('hora', models.TimeField(verbose_name='Hora')),
                ('tipo', models.CharField(max_length=20, verbose_name='Egreso', choices=[('sano', 'Sano'), ('traslado', 'Traslado'), ('con patologia', 'Con patologia'), ('fallece', 'Fallece')])),
                ('ant_ligadura_tubaria', models.BooleanField(default=False, verbose_name='Ligadura Tubaria')),
                ('ant_anticoncec_combinada', models.BooleanField(default=False, verbose_name='Anticoncec. Combinada')),
                ('ant_abstinencia_periodica', models.BooleanField(default=False, verbose_name='Abstinen. Periodica')),
                ('ant_mela', models.BooleanField(default=False, verbose_name='MELA')),
                ('ant_solo_ori_consej', models.BooleanField(default=False, verbose_name='Solo Ori/Consej')),
                ('ant_condon', models.BooleanField(default=False, verbose_name='Cond\xf3n')),
                ('ant_inyectables', models.BooleanField(default=False, verbose_name='Progestag. Inyectables')),
                ('ant_ninguno', models.BooleanField(default=False, verbose_name='Ninguno')),
                ('ant_diu', models.BooleanField(default=False, verbose_name='DIU')),
                ('ant_orales', models.BooleanField(default=False, verbose_name='Progestag. Orales')),
                ('ant_otro', models.BooleanField(default=False, verbose_name='Otro')),
                ('ant_observaciones', models.TextField(null=True, verbose_name='Observaci\xf3n', blank=True)),
                ('control_puerperio', models.DateField(null=True, verbose_name='Control puerperio', blank=True)),
                ('cetficiado_nacido_vivo', models.NullBooleanField(default=None, verbose_name='Certificado de nacido vivo')),
                ('certificado_nacido_vivo_numero', models.IntegerField(null=True, verbose_name='N\xfamero', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('centro_salud', models.ForeignKey(blank=True, to='establecimientos.Establecimiento', null=True)),
                ('creator', models.ForeignKey(related_name='terminacion_puerpera_c', to=settings.AUTH_USER_MODEL)),
                ('establecimiento', models.ForeignKey(related_name='terminacion_puerpera_establecimiento', to='establecimientos.Establecimiento')),
                ('ingreso', models.OneToOneField(related_name='terminacion_puerpera_gestante', to='partos.Ingreso')),
                ('modifier', models.ForeignKey(related_name='terminacion_puerpera_m', to=settings.AUTH_USER_MODEL)),
                ('monitoreo', models.ForeignKey(related_name='monitoreo', to='puerperio.Monitoreo')),
                ('paciente', models.ForeignKey(related_name='terminacion_puerpera_egresos', to='pacientes.Paciente')),
                ('terminacion_embarazo', models.OneToOneField(related_name='terminacion_puerpera_gestante', to='partos.TerminacionEmbarazo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='egresogestante',
            name='ant_observaciones',
            field=models.TextField(null=True, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitoreo',
            name='establecimiento',
            field=models.ForeignKey(related_name='monitoreos', to='establecimientos.Establecimiento', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitoreomedicion',
            name='alojamiento_conjunto',
            field=models.NullBooleanField(default=None, verbose_name='Alojamiento conjunto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitoreomedicion',
            name='alojamiento_conjunto_observacion',
            field=models.TextField(null=True, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitoreomedicion',
            name='contacto_piel',
            field=models.NullBooleanField(default=None, verbose_name='Contacto piel a piel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitoreomedicion',
            name='contacto_piel_observacion',
            field=models.TextField(null=True, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitoreomedicion',
            name='lab_elisa',
            field=models.CharField(default='no aplica', max_length=20, verbose_name='ELISA', choices=[('reactivo', 'Reactivo'), ('no reactivo', 'No reactivo'), ('no se hizo', 'No se hizo'), ('no aplica', 'No aplica')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitoreomedicion',
            name='lab_elisa_fecha',
            field=models.DateField(null=True, verbose_name='Fecha', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitoreomedicion',
            name='lab_fecha_hemoglobina',
            field=models.DateField(null=True, verbose_name='Fecha', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitoreomedicion',
            name='lab_hemoglobina_post_parto',
            field=models.FloatField(blank=True, null=True, verbose_name='Hemoglobina post parto', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitoreomedicion',
            name='lab_rpr',
            field=models.CharField(default='no aplica', max_length=20, verbose_name='RPR', choices=[('reactivo', 'Reactivo'), ('no reactivo', 'No reactivo'), ('no se hizo', 'No se hizo'), ('no aplica', 'No aplica')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitoreomedicion',
            name='lab_rpr_fecha',
            field=models.DateField(null=True, verbose_name='Fecha', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitoreomedicion',
            name='via_periferica',
            field=models.NullBooleanField(default=None, verbose_name='V\xeda perif\xe9rica'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitoreomedicion',
            name='vp_cantidad',
            field=models.FloatField(blank=True, null=True, verbose_name='Cantidad', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitoreomedicion',
            name='vp_oxitocina',
            field=models.NullBooleanField(default=None, verbose_name='Oxitocina'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitoreomedicion',
            name='vp_tipo_de_solucion',
            field=models.CharField(max_length=30, null=True, verbose_name='Tipo de soluci\xf3n', choices=[('cl na', 'Cl Na'), ('dextroza', 'Dextroza'), ('hemacell', 'Hemacell')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='monitoreomedicion',
            name='episeotomia_caracteristicas',
            field=models.CharField(max_length=30, null=True, verbose_name='Caracteristicas', choices=[('bordes afrontados', 'Bordes afrontados'), ('bordes no afrontados', 'Bordes no afrontados'), ('doloroso', 'Doloroso'), ('purulento', 'Purulento'), ('infectada', 'Infectada'), ('flogosis', 'Flogosis'), ('sin dolor', 'Sin dolor')]),
            preserve_default=True,
        ),
    ]
