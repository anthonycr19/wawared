from datetime import datetime, timedelta

from django.test import TestCase
from django.test.utils import override_settings
from mixer.backend.django import mixer
from citas.models import Cita

from establecimientos.models import Establecimiento
from pacientes.models import Paciente


class CitaTestCase(TestCase):
    @override_settings(USE_TZ=False)
    def setUp(self):
        self.paciente = mixer.blend(Paciente)
        self.establecimiento = mixer.blend(Establecimiento)
        self.establecimiento_2 = mixer.blend(Establecimiento)
        fecha = datetime(2014, 1, 1, 8, 0)
        self.cita = Cita.objects.create(
            paciente=self.paciente,
            establecimiento=self.establecimiento,
            fecha=fecha,
            tipo=Cita.TIPO_GESTACION,
            is_wawared=False
        )
        self.cita = Cita.objects.create(
            paciente=self.paciente,
            establecimiento=self.establecimiento,
            fecha=fecha + timedelta(minutes=30),
            tipo=Cita.TIPO_GESTACION,
            is_wawared=False
        )

    def test_existe_para_la_misma_fecha(self):
        result = Cita.exists_cita_in_same_date(
            self.establecimiento, self.cita.fecha)
        self.assertTrue(result)

    def test_no_existe_para_diferente_establecimiento(self):
        result = Cita.exists_cita_in_same_date(
            self.establecimiento_2, self.cita.fecha)
        self.assertFalse(result)

    def test_no_existe_para_diferente_dia(self):
        new_date = self.cita.fecha + timedelta(days=1)
        result = Cita.exists_cita_in_same_date(self.establecimiento, new_date)
        self.assertFalse(result)

    def test_existe_para_hora_dentro_del_rango(self):
        new_date = datetime(2014, 1, 1, 8, 10)
        result = Cita.exists_cita_in_same_date(self.establecimiento, new_date)
        self.assertTrue(result)

    def test_no_existe_para_hora_fuera_del_rango(self):
        new_date = datetime(2014, 1, 1, 7, 30)
        result = Cita.exists_cita_in_same_date(self.establecimiento, new_date)
        self.assertFalse(result)

    def test_existe_para_la_misma_hora(self):
        new_date = datetime(2014, 1, 1, 8, 0)
        result = Cita.exists_cita_in_same_date(self.establecimiento, new_date)
        self.assertTrue(result)

    def test_existe_para_la_hora_de_termino_de_cita(self):
        new_date = datetime(2014, 1, 1, 8, 30)
        result = Cita.exists_cita_in_same_date(self.establecimiento, new_date)
        self.assertTrue(result)
