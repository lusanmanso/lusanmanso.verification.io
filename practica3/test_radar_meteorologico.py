from unittest import TestCase
from radar_meteorologico import alcance_del_radar

class TestRadarMeteorologico(TestCase):

    def test_valores_validos(self):
        """ Test de valores validos """
        self.assertAlmostEqual(alcance_del_radar(0.5, 2), 74999.700)

    def test_valores_fuera_rango(self):
        """ Test ValueError cuando hay valores positivos fuera de rango """
        self.assertRaises(ValueError, alcance_del_radar, 0.2, 5.0)

    def test_valores_negativos(self):
        """ Test ValueError cuando hay de valores negativos """
        raise Exception("no implementado")

    def test_T_menor_tau(self):
        """ Test ValueError cuando T es menor que tau """
        raise Exception("no implementado")

    def test_strings(self):
        """ Test TypeError cuando hay entrada de strings """
        raise Exception("no implementado")

    def test_booleanos(self):
        """ Test TypeError cuando hay entrada de booleanos """
        raise Exception("no implementado")

        


