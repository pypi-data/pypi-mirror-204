import unittest
from math import floor, ceil
from measuring_tools.length import Length

class TestLength(unittest.TestCase):
    
    def test_invalid_measurement(self):
        with self.assertRaises(ValueError):
            Length(0, 'asdf')

####################################################################################

    def test_yard_to_yard_same_obj(self):
        y1 = Length(0, 'yard')
        y2 = y1.to_yard()
        self.assertIs(y1, y2)

    def test_meter_to_meter_same_obj(self):
        m1 = Length(0, 'meter')
        m2 = m1.to_meter()
        self.assertIs(m1, m2)

    def test_mile_to_mile_same_obj(self):
        mile1 = Length(0, 'mile')
        mile2 = mile1.to_mile()
        self.assertIs(mile1, mile2)

    def test_kilometer_to_kilometer_same_obj(self):
        km1 = Length(0, 'kilometer')
        km2 = km1.to_kilometer()
        self.assertIs(km1, km2)

####################################################################################

    def test_abs(self):
        y1 = Length(-5.0, 'yard')
        y2 = Length(5.0, 'yard')
        self.assertEqual(abs(y1), y2)

    def test_floor(self):
        len1 = Length(7.7, 'yard')
        len2 = Length(7.0, 'yard')
        self.assertEqual(floor(len1), len2)

    def test_ceil(self):
        len1 = Length(4.2, 'yard')
        len2 = Length(5.0, 'yard')
        self.assertEqual(ceil(len1), len2)

    def test_inplace_add(self):
        len1 = Length(5.0, 'yard')
        len1 += 3.0
        self.assertEqual(len1.value, 8.0)
    
    def test_inplace_sub(self):
        len1 = Length(5.0, 'yard')
        len1 -= 3.0
        self.assertEqual(len1.value, 2.0)

    def test_inplace_mul(self):
        len1 = Length(5.0, 'yard')
        len1 *= 3.0
        self.assertEqual(len1.value, 15.0)        

    def test_inplace_div(self):
        len1 = Length(9.0, 'yard')
        len1 /= 3.0
        self.assertEqual(len1.value, 3.0)

    def test_inplace_floordiv(self):
        len1 = Length(8.0, 'yard')
        len1 //= 3.0
        self.assertEqual(len1.value, 2.0)

    def test_inplace_modulo(self):
        len1 = Length(18.0, 'yard')
        len1 %= 4.0
        self.assertEqual(len1.value, 2.0)

####################################################################################

    def test_yard_meter_equal_value(self):
        y = Length(5.123, 'yard')
        m = Length(4.68447, 'meter')
        self.assertEqual(m, y)

    def test_yard_mile_equal_value(self):
        y = Length(500, 'yard')
        mile = Length(0.28409, 'mile')
        self.assertEqual(y, mile)

    def test_yard_kilometer_equal_value(self):
        y = Length(500, 'yard')
        km = Length(0.4572, 'kilometer')
        self.assertEqual(y, km)

    def test_meter_yard_equal_value(self):
        y = Length(5.12299, 'yard')
        m = Length(4.68447, 'meter')
        self.assertEqual(y, m)

    def test_meter_mile_equal_value(self):
        m = Length(500, 'meter')
        mile = Length(0.3106856, 'mile')
        self.assertEqual(m, mile)

    def test_meter_kilometer_equal_value(self):
        m = Length(500, 'meter')
        km = Length(0.5, 'kilometer')
        self.assertEqual(m, km)

    def test_mile_yard_equal_value(self):
        y = Length(500, 'yard')
        mile = Length(0.28409, 'mile')
        self.assertEqual(mile, y)

    def test_mile_meter_equal_value(self):
        m = Length(500, 'meter')
        mile = Length(0.3106856, 'mile')
        self.assertEqual(mile, m)

    def test_mile_kilometer_equal_value(self):
        mile = Length(500, 'mile')
        km = Length(804.672, 'kilometer')
        self.assertEqual(mile, km)

    def test_kilometer_yard_equal_value(self):
        y = Length(500, 'yard')
        km = Length(0.4572, 'kilometer')
        self.assertEqual(km, y)

    def test_kilometer_meter_equal_value(self):
        m = Length(500, 'meter')
        km = Length(0.5, 'kilometer')
        self.assertEqual(km, m)

    def test_kilometer_mile_equal_value(self):
        mile = Length(500, 'mile')
        km = Length(804.672, 'kilometer')
        self.assertEqual(km, mile)

####################################################################################

    def test_yard_lt_meter(self):
        len1 = Length(5, 'yard')
        len2 = Length(5, 'meter')
        self.assertLess(len1, len2)

    def test_meter_lt_yard(self):
        len1 = Length(5, 'meter')
        len2 = Length(100, 'yard')
        self.assertLess(len1, len2)

    def test_mile_lt_kilometer(self):
        len1 = Length(5, 'mile')
        len2 = Length(20, 'kilometer')
        self.assertLess(len1, len2)

    def test_kilometer_lt_mile(self):
        len1 = Length(5, 'kilometer')
        len2 = Length(20, 'mile')
        self.assertLess(len1, len2)

#####################################################################################

    def test_yard_gt_meter(self):
        y = Length(50, 'yard')
        m = Length(5, 'meter')
        self.assertGreater(y, m)

    def test_meter_gt_yard(self):
        y = Length(5, 'yard')
        m = Length(50, 'meter')
        self.assertGreater(m, y)

#####################################################################################

    def test_meter_add_yard(self):
        len1 = Length(5, 'meter')
        len2 = Length(5, 'yard')
        result = len1 + len2
        self.assertAlmostEqual(result.value, 9.572, places=5)

    def test_yard_add_meter(self):
        len1 = Length(5, 'yard')
        len2 = Length(5, 'meter')
        result = len1 + len2
        self.assertAlmostEqual(result.value, 10.468066, places=5)

    def test_meter_sub_yard(self):
        len1 = Length(5, 'meter')
        len2 = Length(2, 'yard')
        result = len1 - len2
        self.assertAlmostEqual(result.value, 3.1712, places=5)

    def test_yard_sub_meter(self):
        len1 = Length(10, 'yard')
        len2 = Length(5, 'meter')
        result = len1 - len2
        self.assertAlmostEqual(result.value, 4.53193, places=5)

    def test_yard_mul_meter(self):
        len1 = Length(5, 'yard')
        len2 = Length(5, 'meter')
        result = len1 * len2
        self.assertAlmostEqual(result.value, 27.34033, places=5)

    def test_meter_mul_yard(self):
        len1 = Length(5, 'meter')
        len2 = Length(5, 'yard')
        result = len1 * len2
        self.assertAlmostEqual(result.value, 22.86)

    def test_yard_div_meter(self):
        len1 = Length(5, 'yard')
        len2 = Length(5, 'meter')
        result = len1 / len2
        self.assertAlmostEqual(result.value, 0.9144, places=5)

    def test_meter_div_yard(self):
        len1 = Length(5, 'meter')
        len2 = Length(5, 'yard')
        result = len1 / len2
        self.assertAlmostEqual(result.value, 1.09361, places=5)

    def test_yard_floor_meter(self):
        len1 = Length(5, 'yard')
        len2 = Length(5, 'meter')
        result = len1 // len2
        self.assertEqual(result.value, 0.0)

    def test_meter_floor_yard(self):
        len1 = Length(5, 'meter')
        len2 = Length(5, 'yard')
        result = len1 // len2
        self.assertEqual(result.value, 1.0)

    def test_meter_mod_yard(self):
        len1 = Length(18, 'meter')
        len2 = Length(4, 'yard')
        result = len1 % len2
        self.assertAlmostEqual(result.value, 3.3696)
