# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
from time import sleep
from os import path

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from cpt.models import CatalogoProcedimiento


class Command(BaseCommand):
    help = 'Importa los datos CPT de un file CSV al modelo CPT de Wawared'
    option_list = BaseCommand.option_list + (
        make_option(
            "-f",
            "--file",
            dest="filename",
            help="Archivo CSV a Importar a Wawared",
            metavar="FILE"
        ),
    )

    def handle(self, *args, **options):

        if options['filename'] == None:
            raise CommandError("Option `--file=...` debe especificar un valor para este parametro.")

        if not path.isfile(options['filename']):
            raise CommandError("El archivo no existe en la ruta especificada.")

        CatalogoProcedimiento.objects.all().delete()
        with open(options['filename']) as f:
            reader = csv.reader(f, dialect=csv.excel)
            i = 1
            for row in reader:

                if i > 1:
                    created = CatalogoProcedimiento.objects.get_or_create(
                        codigo_cpt=row[0],
                        denominacion_procedimientos=row[1],
                        sexo=row[2]
                    )

                i = i + 1

        self.stdout.write("Se Importo correctamente el archivo")
        # espera antes de continuar
        sleep(0.1)
