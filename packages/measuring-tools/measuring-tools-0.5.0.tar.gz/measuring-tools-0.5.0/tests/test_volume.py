import unittest
from math import floor, ceil
from measuring_tools.volume import Volume

class TestVolume(unittest.TestCase):

    def test_invalid_measurement(self):
        with self.assertRaises(ValueError):
            Volume(0, 'asdf')

####################################################################################

    def test_liter_to_liter_same_obj(self):
        l1 = Volume(0, 'liter')
        l2 = l1.to_liter()
        self.assertIs(l1, l2)

    def test_gallon_to_gallon_same_obj(self):
        g1 = Volume(0, 'gallon')
        g2 = g1.to_gallon()
        self.assertIs(g1, g2)

    def test_gallon_us_to_gallon_us_same_obj(self):
        g1 = Volume(0, 'gallon_us')
        g2 = g1.to_gallon_us()
        self.assertIs(g1, g2)

####################################################################################

    def test_abs(self):
        v1 = Volume(-5.0, 'liter')
        v2 = Volume(5.0, 'liter')
        self.assertEqual(abs(v1), v2)

    def test_floor(self):
        v1 = Volume(7.7, 'liter')
        v2 = Volume(7.0, 'liter')
        self.assertEqual(floor(v1), v2)

    def test_ceil(self):
        v1 = Volume(4.2, 'liter')
        v2 = Volume(5.0, 'liter')
        self.assertEqual(ceil(v1), v2)

    def test_inplace_add(self):
        vol1 = Volume(5.0, 'liter')
        vol1 += 3.0
        self.assertEqual(vol1.value, 8.0)
    
    def test_inplace_sub(self):
        vol1 = Volume(5.0, 'liter')
        vol1 -= 3.0
        self.assertEqual(vol1.value, 2.0)

    def test_inplace_mul(self):
        vol1 = Volume(5.0, 'liter')
        vol1 *= 3.0
        self.assertEqual(vol1.value, 15.0)        

    def test_inplace_div(self):
        vol1 = Volume(9.0, 'liter')
        vol1 /= 3.0
        self.assertEqual(vol1.value, 3.0)

    def test_inplace_floordiv(self):
        vol1 = Volume(8.0, 'liter')
        vol1 //= 3.0
        self.assertEqual(vol1.value, 2.0)

    def test_inplace_modulo(self):
        vol1 = Volume(18.0, 'liter')
        vol1 %= 4.0
        self.assertEqual(vol1.value, 2.0)

####################################################################################

    def test_liter_gallon_equal_value(self):
        l = Volume(5, 'liter')
        g = Volume(1.0998462, 'gallon')
        self.assertEqual(l, g)

    def test_liter_gallon_us_equal_value(self):
        l = Volume(5, 'liter')
        g = Volume(1.32086, 'gallon_us')
        self.assertEqual(l, g)

    def test_gallon_liter_equal_value(self):
        l = Volume(5, 'liter')
        g = Volume(1.0998462, 'gallon')
        self.assertEqual(g, l)

    def test_gallon_gallon_us_equal_value(self):
        g = Volume(5, 'gallon')
        gus = Volume( 6.0047496, 'gallon_us')
        self.assertEqual(g, gus)

    def test_gallon_us_liter_equal_value(self):
        l = Volume(5, 'liter')
        g = Volume(1.32086, 'gallon_us')
        self.assertEqual(g, l)

    def test_gallon_us_gallon_equal_value(self):
        g = Volume(5, 'gallon')
        gus = Volume(6.0047496, 'gallon_us')
        self.assertEqual(gus, g)

####################################################################################

    def test_liter_lt_gallon(self):
        l = Volume(50, 'liter')
        g = Volume(50, 'gallon')
        self.assertLess(l, g)

    def test_liter_lt_gallon_us(self):
        l = Volume(50, 'liter')
        gus = Volume(50, 'gallon_us')
        self.assertLess(l, gus)

    def test_gallon_lt_liter(self):
        l = Volume(50, 'liter')
        g = Volume(10, 'gallon')
        self.assertLess(g, l)

    def test_gallon_lt_gallon_us(self):
        g = Volume(50, 'gallon')
        gus = Volume(60.5, 'gallon_us')
        self.assertLess(g, gus)

    def test_gallon_us_lt_liter(self):
        l = Volume(190, 'liter')
        gus = Volume(50, 'gallon_us')
        self.assertLess(gus, l)

    def test_gallon_us_lt_gallon(self):
        g = Volume(50, 'gallon')
        gus = Volume(50, 'gallon_us')
        self.assertLess(gus, g)

####################################################################################

    def test_liter_gt_gallon(self):
        l = Volume(50, 'liter')
        g = Volume(10.5, 'gallon')
        self.assertGreater(l, g)

    def test_liter_gt_gallon_us(self):
        l = Volume(50, 'liter')
        gus = Volume(13, 'gallon_us')
        self.assertGreater(l, gus)

    def test_gallon_gt_liter(self):
        l = Volume(50, 'liter')
        g = Volume(50, 'gallon')
        self.assertGreater(g, l)

    def test_gallon_gt_gallon_us(self):
        g = Volume(50, 'gallon')
        gus = Volume(50, 'gallon_us')
        self.assertGreater(g, gus)

    def test_gallon_us_gt_liter(self):
        l = Volume(50, 'liter')
        gus = Volume(50, 'gallon_us')
        self.assertGreater(gus, l)

    def test_gallon_us_gt_gallon(self):
        g = Volume(41, 'gallon')
        gus = Volume(50, 'gallon_us')
        self.assertGreater(gus, g)

    def test_liter_mod_gallon_us(self):
        l = Volume(115, 'liter')
        gus = Volume(20, 'gallon_us')
        result = l % gus
        self.assertAlmostEqual(result.value, 39.2917644)