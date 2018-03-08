# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0001_initial'),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, max_length=255, db_index=True)),
                ('email', models.EmailField(max_length=255)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('type', models.CharField(default=b'medico', max_length=10, verbose_name=b'Tipo de usuario', choices=[(b'medico', b'Medico'), (b'licenciado', b'Obstetra')])),
                ('dni', models.CharField(blank=True, max_length=8, null=True, verbose_name=b'DNI', validators=[django.core.validators.RegexValidator(regex=b'^\\d{8}$', message='El n\xfamero de DNI debe contener 8 d\xedgitos')])),
                ('his', models.CharField(blank=True, max_length=8, null=True, verbose_name=b'HIS', validators=[django.core.validators.RegexValidator(regex=b'^\\d{8}$', message='El n\xfamero de HIS debe contener 8 d\xedgitos')])),
                ('colegiatura', models.CharField(blank=True, max_length=20, null=True, verbose_name=b'Colegiatura', validators=[django.core.validators.RegexValidator(regex=b'^\\d{5}\\d+$', message='El n\xfamero de colegiatura debe contener al menos 6 d\xedgitos')])),
                ('establecimiento', models.ForeignKey(verbose_name=b'Establecimiento origen', blank=True, to='establecimientos.Establecimiento', null=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsuarioEstablecimiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('establecimientos', models.ManyToManyField(to='establecimientos.Establecimiento', null=True, blank=True)),
                ('usuario', models.ForeignKey(verbose_name=b'Usuario', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
            bases=(models.Model,),
        ),
    ]
