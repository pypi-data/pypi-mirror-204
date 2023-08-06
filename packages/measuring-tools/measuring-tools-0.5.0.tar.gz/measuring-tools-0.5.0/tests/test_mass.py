import unittest
from math import floor, ceil
from measuring_tools.mass import Mass

class TestMass(unittest.TestCase):

    def test_invalid_measurement(self):
        with self.assertRaises(ValueError):
            Mass(0, 'asdf')

####################################################################################

    def test_pound_to_pound_same_obj(self):
        p1 = Mass(0, 'pound')
        p2 = p1.to_pound()
        self.assertIs(p1, p2)

    def test_gram_to_gram_same_obj(self):
        g1 = Mass(0, 'gram')
        g2 = g1.to_gram()
        self.assertIs(g1, g2)

    def test_ton_us_to_ton_us_same_obj(self):
        ton_us1 = Mass(0, 'ton_us')
        ton_us2 = ton_us1.to_ton_us()
        self.assertIs(ton_us1, ton_us2)

    def test_kilogram_to_kilogram_same_obj(self):
        kg1 = Mass(0, 'kilogram')
        kg2 = kg1.to_kilogram()
        self.assertIs(kg1, kg2)

####################################################################################

    def test_abs(self):
        m1 = Mass(-5.0, 'pound')
        m2 = Mass(5.0, 'pound')
        self.assertEqual(abs(m1), m2)

    def test_floor(self):
        m1 = Mass(7.7, 'pound')
        m2 = Mass(7.0, 'pound')
        self.assertEqual(floor(m1), m2)

    def test_ceil(self):
        m1 = Mass(4.2, 'pound')
        m2 = Mass(5.0, 'pound')
        self.assertEqual(ceil(m1), m2)

    def test_inplace_add(self):
        m1 = Mass(5.0, 'pound')
        m1 += 3.0
        self.assertEqual(m1.value, 8.0)

    def test_inplace_sub(self):
        m1 = Mass(5.0, 'pound')
        m1 -= 3.0
        self.assertEqual(m1.value, 2.0)

    def test_inplace_mul(self):
        m1 = Mass(5.0, 'pound')
        m1 *= 3.0
        self.assertEqual(m1.value, 15.0)

    def test_inplace_div(self):
        m1 = Mass(9.0, 'pound')
        m1 /= 3.0
        self.assertEqual(m1.value, 3.0)

    def test_inplace_floordiv(self):
        m1 = Mass(8.0, 'pound')
        m1 //= 3.0
        self.assertEqual(m1.value, 2.0)

    def test_inplace_modulo(self):
        m1 = Mass(18.0, 'pound')
        m1 %= 4.0
        self.assertEqual(m1.value, 2.0)

#####################################################################################

    def test_kilogram_mod_pound(self):
        m1 = Mass(18, 'kilogram')
        m2 = Mass(4, 'pound')
        result = m1 % m2
        self.assertAlmostEqual(result.value, 0.363019)