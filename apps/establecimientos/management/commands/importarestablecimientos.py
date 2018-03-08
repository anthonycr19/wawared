# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
from time import sleep
from os import path
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from establecimientos.models import Establecimiento, Diresa, Red, Microred


class Command(BaseCommand):
    help = 'Importa los datos de establecimientos de un file CSV al modelo establecimientos.Establecimiento de Wawared'
    option_list = BaseCommand.option_list + (
        make_option(
            "-f",
            "--file",
            dest="filename",
            help="Archivo CSV de establecimientos a importar a Wawared",
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
                    if Establecimiento.objects.filter(codigo=row[0]).count() == 0:

                        if Diresa.objects.filter(nombre=row[3]).count() == 0:
                            diresa = Diresa.objects.create(nombre=row[3])
                        else:
                            diresa = Diresa.objects.get(nombre=row[3])

                        if Red.objects.filter(nombre=row[4], diresa=diresa).count() == 0:
                            red = Red.objects.create(nombre=row[4], diresa=diresa)
                        else:
                            red = Red.objects.get(nombre=row[4], diresa=diresa)

                        if Microred.objects.filter(nombre=row[5], red=red).count() == 0:
                            microred = Microred.objects.create(nombre=row[5], red=red)
                        else:
                            microred = Microred.objects.get(nombre=row[5], red=red)

                        newtel = unicode(row[2], errors='ignore').split('-')[0]
                        establecimiento = Establecimiento(diresa=diresa, red=red, microred=microred,
                                                          telefono=newtel[0:20 if len(newtel) > 20 else len(newtel)],
                                                          nombre=row[1], codigo=row[0])
                        try:
                            establecimiento.save()
                            self.stdout.write(
                                "Sucess: Se Importo correctamente el establecimiento %s" % establecimiento.codigo)
                        except IntegrityError:
                            self.stdout.write("Sucess: Error al importar el establecimiento %s" % row[0])

                i = i + 1
        # espera antes de continuar
        sleep(0.1)
