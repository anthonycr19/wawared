# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, transaction
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('partos', '0005_auto_20170920_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='Placenta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('placenta_desprendimiento', models.CharField(default='-', max_length=1, null=True, verbose_name='Desprendimiento', choices=[('-', '----'), ('C', 'Completa'), ('I', 'Incompleta')])),
                ('placenta_tipo', models.CharField(default='----', max_length=20, null=True, verbose_name='Tipo', choices=[('----', '----'), ('shultz', 'Shultz'), ('duncan', 'Duncan')])),
                ('placenta_peso', models.IntegerField(default=0, null=True, verbose_name='Peso', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)])),
                ('placenta_tamanio_ancho', models.IntegerField(default=0, null=True, verbose_name='Ancho', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)])),
                ('placenta_tamanio_longitud', models.IntegerField(default=0, null=True, verbose_name='Longitud', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)])),
                ('placenta_otras_caracteristicas', models.TextField(null=True, verbose_name='Otras caracter\xedsticas', blank=True)),
                ('membranas', models.CharField(default='----', max_length=1, null=True, verbose_name='Membranas', choices=[('-', '----'), ('C', 'Completa'), ('I', 'Incompleta')])),
                ('cordon_umbilical_longitud', models.IntegerField(default=0, null=True, verbose_name='Longitud', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)])),
                ('cordon_umbilical_diametro', models.IntegerField(default=0, null=True, verbose_name='Diametro', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('cordon_umbilical_insercion', models.CharField(blank=True, max_length=22, null=True, verbose_name='Inserci\xf3n', choices=[('central', 'Central'), ('excentrica', 'Excentrica'), ('marginal (en raqueta)', 'Marginal (Raqueta)'), ('velamentosa', 'Velamentosa')])),
                ('cordon_umbilical_vasos', models.CharField(blank=True, max_length=20, null=True, verbose_name='Vasos', choices=[('1 vena y 2 arterias', '1 vena y 2 arterias'), ('otro', 'Otro')])),
                ('cordon_umbilical_circular', models.CharField(blank=True, max_length=1, null=True, verbose_name='Circular', choices=[('s', 'Si'), ('n', 'No')])),
                ('cordon_umbilical_circular_tipo', models.CharField(blank=True, max_length=10, null=True, verbose_name='Tipo', choices=[('simple', 'Simple'), ('doble', 'Doble'), ('triple', 'Triple')])),
                ('cordon_umbilical_otras_caracteristicas', models.TextField(null=True, verbose_name='Otras caracter\xedsticas', blank=True)),
                ('liquido_amniotico_cantidad', models.IntegerField(default=0, null=True, verbose_name='Cantidad', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)])),
                ('liquido_amniotico_color', models.CharField(default='----', max_length=20, null=True, verbose_name='Color', choices=[('----', '----'), ('claro', 'Claro'), ('meconial', 'Meconial'), ('sanguinolento', 'Sanguinolento')])),
                ('liquido_amniotico_olor', models.CharField(default='----', max_length=20, null=True, verbose_name='Olor', choices=[('----', '----'), ('fuerte', 'Fuerte'), ('suave', 'Suave')])),
                ('otras_caracteristicas', models.TextField(null=True, verbose_name='Otras caracter\xedsticas', blank=True)),
                ('terminacion_embarazo', models.ForeignKey(related_name='placentas', blank=True, to='partos.TerminacionEmbarazo', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='reciennacido',
            name='terminacion_embarazo',
        ),
        migrations.DeleteModel(
            name='RecienNacido',
        ),
        migrations.RemoveField(
            model_name='terminacionembarazo',
            name='desgarros',
        ),
        migrations.RemoveField(
            model_name='terminacionembarazo',
            name='duracion_parto_perdiodo_1',
        ),
        migrations.RemoveField(
            model_name='terminacionembarazo',
            name='duracion_parto_perdiodo_2',
        ),
        migrations.RemoveField(
            model_name='terminacionembarazo',
            name='duracion_parto_perdiodo_3',
        ),
        migrations.AddField(
            model_name='partogramamedicion',
            name='observaciones',
            field=models.TextField(null=True, verbose_name='Observaciones', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='desgarro',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Desgarro', choices=[('s', 'Si'), ('n', 'No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='desgarro_grado',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Grado', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='dirigido_parto_periodo_3',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Dirigido', choices=[('s', 'Si'), ('n', 'No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='duracion_parto_perdiodo_1_horas',
            field=models.IntegerField(blank=True, null=True, verbose_name='1er periodo', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(48)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='duracion_parto_perdiodo_1_minutos',
            field=models.IntegerField(blank=True, null=True, verbose_name='', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(60)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='duracion_parto_perdiodo_2_horas',
            field=models.IntegerField(blank=True, null=True, verbose_name='2do periodo', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(48)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='duracion_parto_perdiodo_2_minutos',
            field=models.IntegerField(blank=True, null=True, verbose_name='', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(60)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='duracion_parto_perdiodo_3_horas',
            field=models.IntegerField(blank=True, null=True, verbose_name='3er periodo', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(48)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='duracion_parto_perdiodo_3_minutos',
            field=models.IntegerField(blank=True, null=True, verbose_name='', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(60)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='hora_1_parto_periodo_2',
            field=models.TimeField(null=True, verbose_name='Hora', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='hora_2_parto_periodo_2',
            field=models.TimeField(null=True, verbose_name='Hora 2', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='hora_3_parto_periodo_2',
            field=models.TimeField(null=True, verbose_name='Hora 3', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='hora_4_parto_periodo_2',
            field=models.TimeField(null=True, verbose_name='Hora 4', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='hora_5_parto_periodo_2',
            field=models.TimeField(null=True, verbose_name='Hora 5', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='hora_parto_periodo_3',
            field=models.TimeField(null=True, verbose_name='Hora', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='inicio_parto_periodo_1',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Inicio', choices=[('espontaneo', 'Espontaneo'), ('inducido', 'Inducido'), ('estimulado', 'Estimulado')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='inicio_parto_periodo_2',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Inicio', choices=[('espontaneo', 'Espontaneo'), ('inducido', 'Inducido'), ('estimulado', 'Estimulado')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='sangrado_aproximado',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Sangrado aproximado', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='terminacionembarazo',
            name='tipo_episiotomia',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Tipo', choices=[('M', 'M'), ('MLD', 'MLD'), ('MLI', 'MLI')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partogramamedicion',
            name='moldeaminetos',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Moldeamientos', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partogramamedicion',
            name='orina_volumen',
            field=models.IntegerField(blank=True, null=True, verbose_name='Volumen', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partogramamedicion',
            name='tv_descenso_cefalico',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Descenso cef\xe1lico', choices=[('5', '5/5'), ('4', '4/5'), ('3', '3/5'), ('2', '2/5'), ('1', '1/5'), ('0', '0/5')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='terminacionembarazo',
            name='episiotomia',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Episiotom\xeda', choices=[('s', 'Si'), ('n', 'No')]),
            preserve_default=True,
        ),
    ]
