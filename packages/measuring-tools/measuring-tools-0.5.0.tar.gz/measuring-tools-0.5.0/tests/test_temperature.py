import unittest
from math import floor, ceil
from measuring_tools.temperature import Temperature

class TestTemperature(unittest.TestCase):

    def test_invalid_measurement(self):
        with self.assertRaises(ValueError):
            Temperature(0, 'asdf')

####################################################################################

    def test_fahrenheit_to_fahrenheit_same_obj(self):
        f1 = Temperature(0)
        f2 = f1.to_fahrenheit()
        self.assertIs(f1, f2)

    def test_celsius_to_celsius_same_obj(self):
        c1 = Temperature(0, 'celsius')
        c2 = c1.to_celsius()
        self.assertIs(c1, c2)

    def test_kelvin_to_kelvin_same_obj(self):
        k1 = Temperature(0, 'kelvin')
        k2 = k1.to_kelvin()
        self.assertIs(k1, k2)

####################################################################################

    def test_abs(self):
        f1 = Temperature(-30.0)
        f2 = Temperature(30.0)
        self.assertEqual(abs(f1), f2)

    def test_floor(self):
        f1 = Temperature(7.7)
        f2 = Temperature(7.0)
        self.assertEqual(floor(f1), f2)

    def test_ceil(self):
        f1 = Temperature(4.2)
        f2 = Temperature(5.0)
        self.assertEqual(ceil(f1), f2)

    def test_inplace_add(self):
        f1 = Temperature(1.0)
        f1 += 32.0
        self.assertEqual(f1.value, 33.0)

    def test_inplace_sub(self):
        f1 = Temperature(33.0)
        f1 -= 32.0
        self.assertEqual(f1.value, 1.0)

    def test_inplace_mul(self):
        f1 = Temperature(5.0)
        f1 *= 3
        self.assertEqual(f1.value, 15.0)

    def test_inplace_truediv(self):
        f1 = Temperature(24.0)
        f1 /= 5.0
        self.assertEqual(f1.value, 4.8)

    def test_inplace_floordiv(self):
        f1 = Temperature(24.0)
        f1 //= 5.0
        self.assertEqual(f1.value, 4.0)

    def test_inplace_modulo(self):
        f1 = Temperature(18.0)
        f1 %= 4.0
        self.assertEqual(f1.value, 2.0)

####################################################################################

    def test_fahrenheit_celsius_equal_value(self):
        f = Temperature(34.42141)
        c = Temperature(1.34522, 'celsius')
        self.assertEqual(c, f)

    def test_fahrenheit_kelvin_equal_value(self):
        f = Temperature(34.42141)
        k = Temperature(274.49522, 'kelvin')
        self.assertEqual(k, f)

    def test_clesius_fahrenheit_equal_value(self):
        f = Temperature(34.42141)
        c = Temperature(1.34522, 'celsius')
        self.assertEqual(f, c)

    def test_clesius_kelvin_equal_value(self):
        k = Temperature(274.273, 'kelvin')
        c = Temperature(1.123, 'celsius')
        self.assertEqual(k, c)

    def test_kelvin_fahrenheit_equal_value(self):
        f = Temperature(1.123)
        k = Temperature(255.99611, 'kelvin')
        self.assertEqual(f, k)

    def test_kelvin_clesius_equal_value(self):
        k = Temperature(274.273, 'kelvin')
        c = Temperature(1.123, 'celsius')
        self.assertEqual(c, k)

####################################################################################
    
    def test_fahrenheit_lt_celsius(self):
        f = Temperature(25)
        c = Temperature(75, 'celsius')
        self.assertLess(f, c)

    def test_fahrenheit_lt_kelvin(self):
        f = Temperature(25)
        k = Temperature(500, 'kelvin')
        self.assertLess(f, k)

    def test_celsius_lt_fahrenheit(self):
        c = Temperature(5, 'celsius')
        f = Temperature(75)
        self.assertLess(c, f)

    def test_celsius_lt_kelvin(self):
        c = Temperature(5, 'celsius')
        k = Temperature(500, 'kelvin')
        self.assertLess(c, k)

    def test_kelvin_lt_fahrenheit(self):
        k = Temperature(25, 'kelvin')
        f = Temperature(25)
        self.assertLess(k, f)

    def test_kelvin_lt_celsius(self):
        k = Temperature(25, 'kelvin')
        c = Temperature(25, 'celsius')
        self.assertLess(k, c)

####################################################################################

    def test_fahrenheit_gt_celsius(self):
        f = Temperature(500)
        c = Temperature(25, 'celsius')
        self.assertGreater(f, c)

    def test_fahrenheit_gt_kelvin(self):
        f = Temperature(500)
        k = Temperature(25, 'kelvin')
        self.assertGreater(f, k)

    def test_celsius_gt_fahrenheit(self):
        c = Temperature(75, 'celsius')
        f = Temperature(5)
        self.assertGreater(c, f)

    def test_celsius_gt_kelvin(self):
        c = Temperature(500, 'celsius')
        k = Temperature(5, 'kelvin')
        self.assertGreater(c, k)

    def test_kelvin_gt_fahrenheit(self):
        k = Temperature(2500, 'kelvin')
        f = Temperature(25)
        self.assertGreater(k, f)

    def test_kelvin_gt_celsius(self):
        k = Temperature(2500, 'kelvin')
        c = Temperature(25, 'celsius')
        self.assertGreater(k, c)

####################################################################################

    def test_fahrenheit_add_celsius(self):
        f = Temperature(50)
        c = Temperature(5.1234, 'celsius')
        result = f + c
        self.assertAlmostEqual(result.value, 91.22212)

    def test_fahrenheit_add_kelvin(self):
        f = Temperature(50)
        k = Temperature(500, 'kelvin')
        result = f + k
        self.assertAlmostEqual(result.value, 490.33)

    def test_celsius_add_fahrenheit(self):
        f = Temperature(50.432)
        c = Temperature(5.1234, 'celsius')
        result = c + f
        self.assertAlmostEqual(result.value, 15.3634)

    def test_celsius_add_kelvin(self):
        c = Temperature(2.543, 'celsius')
        k = Temperature(300.8, 'kelvin')
        result = c + k
        self.assertAlmostEqual(result.value, 30.193)

    def test_kelvin_add_fahrenheit(self):
        f = Temperature(50)
        k = Temperature(500, 'kelvin')
        result = k + f
        self.assertAlmostEqual(result.value, 783.15)

    def test_kelvin_add_celsius(self):
        c = Temperature(3.523, 'celsius')
        k = Temperature(293.834, 'kelvin')
        result = k + c
        self.assertAlmostEqual(result.value, 570.507)

    def test_fahrenheit_mod_celsius(self):
        f = Temperature(115, 'fahrenheit')
        c = Temperature(20, 'celsius')
        result = f % c
        self.assertAlmostEqual(result.value, 47.0)