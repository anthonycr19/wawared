# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
from time import sleep
from os import path

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from perfiles.models import User
from establecimientos.models import Establecimiento


class Command(BaseCommand):
    help = 'Importa los datos de usuario de un file CSV al modelo perfiles.User de Wawared'
    option_list = BaseCommand.option_list + (
        make_option(
            "-f",
            "--file",
            dest="filename",
            help="Archivo CSV de usuarios a importar a Wawared",
            metavar="FILE"
        ),
    )

    def handle(self, *args, **options):

        if options['filename'] == None:
            raise CommandError("Option `--file=...` debe especificar un valor para este parametro.")

        if not path.isfile(options['filename']):
            raise CommandError("El archivo no existe en la ruta especificada.")

        with open(options['filename']) as f:
            reader = csv.reader(f, dialect=csv.excel)
            i = 1
            for row in reader:
                if i > 1:
                    if User.objects.filter(username=row[10]).count() == 0:
                        try:
                            user = User(
                                username=row[10],
                                email=row[9],
                                dni=row[10],
                                celular=row[8],
                                establecimiento=Establecimiento.objects.get(codigo=row[5]),
                                type=User.LICENCIADO
                            )
                        except Establecimiento.DoesNotExist:
                            self.stdout.write(
                                "Error: El establecimiento de origen del usuario no esta registrado en Wawared")
                            continue
                    else:
                        user = User.objects.filter(username=row[10]).last()

                    user.first_name = row[6]
                    user.last_name = row[7]
                    user.set_password(row[10])
                    user.save()
                    self.stdout.write("Sucess: Se Importo correctamente el usuario %s" % user.username)

                i = i + 1
        # espera antes de continuar
        sleep(0.1)
