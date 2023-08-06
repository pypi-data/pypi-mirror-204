''' Functionality for teperature conversions and temperature equality checks recorded in Fahrenheit, Celsius,
and Kelvin. Values of two different temperatures recorded in different measurements are considered equal
if the converted values within a relative tolerance or absolute tolerance of FLOAT_POINT_TOL.
The default for FLOAT_POINT_TOL is 1e-05.
'''


import functools
from math import isclose, floor, ceil
from measuring_tools import Measurement


def __dir__():
    return ('Temperature', 'ABSOLUTE_ZERO', 'FREEZING_POINT', 'BOILING_POINT', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__')


@functools.total_ordering
class Temperature(Measurement):
    '''Temperature Converter for Fahrenheit, Celsius, and Kelvin
    * value is expected to be either an integer or a float
    * measurement can be one of three options (defaults to fahrenheit)
        - fahrenheit
        - celsius
        - kelvin
    '''


    def __init__(self, value: int | float, measurement: str='fahrenheit'):
        if not measurement in ('fahrenheit', 'celsius', 'kelvin'):
            raise ValueError('Value must be fahrenheit, celsius, or kelvin')
        super().__init__(value, measurement)


    def __str__(self):
        return f'{self.value} degress {self.measurement}'


    def __round__(self, ndigits):
        return Temperature(round(self.value, ndigits=ndigits), self.measurement)
        
    def __abs__(self):
        return Temperature(abs(self.value), self.measurement)


    def __floor__(self):
        return Temperature(floor(self.value), self.measurement)


    def __ceil__(self):
        return Temperature(ceil(self.value), self.measurement)


    def __eq__(self, other):
        match self.measurement:
            case 'fahrenheit':
                return isclose(self.value, other.to_fahrenheit().value, rel_tol=self.FLOAT_POINT_TOL, abs_tol=self.FLOAT_POINT_TOL)
            case 'celsius':
                return isclose(self.value, other.to_celsius().value, rel_tol=self.FLOAT_POINT_TOL, abs_tol=self.FLOAT_POINT_TOL)
            case 'kelvin':
                return isclose(self.value, other.to_kelvin().value, rel_tol=self.FLOAT_POINT_TOL, abs_tol=self.FLOAT_POINT_TOL)


    def __lt__(self, other):
        if self == other:
            return False
        match self.measurement:
            case 'fahrenheit':
                return self.value < other.to_fahrenheit().value
            case 'celsius':
                return self.value < other.to_celsius().value
            case 'kelvin':
                return self.value < other.to_kelvin().value


    def __add__(self, other):
        match self.measurement:
            case 'fahrenheit':
                total = self.value + other.to_fahrenheit().value
            case 'celsius':
                total = self.value + other.to_celsius().value
            case 'kelvin':
                total = self.value + other.to_kelvin().value
        return Temperature(total, self.measurement)


    def __sub__(self, other):
        match self.measurement:
            case 'fahrenheit':
                diff = self.value - other.to_fahrenheit().value
            case 'celsius':
                diff = self.value - other.to_celsius().value
            case 'kelvin':
                diff = self.value - other.to_kelvin().value
        return Temperature(diff, self.measurement)


    def __mul__(self, other):
        match self.measurement:
            case 'fahrenheit':
                product = self.value * other.to_fahrenheit().value
            case 'celsius':
                product = self.value * other.to_celsius().value
            case 'kelvin':
                product = self.value * other.to_kelvin().value
        return Temperature(product, self.measurement)


    def __truediv__(self, other):
        match self.measurement:
            case 'fahrenheit':
                result = self.value / other.to_fahrenheit().value
            case 'celsius':
                result = self.value / other.to_celsius().value
            case 'kelvin':
                result = self.value / other.to_kelvin().value
        return Temperature(result, self.measurement)


    def __floordiv__(self, other):
        match self.measurement:
            case 'fahrenheit':
                quotient = self.value // other.to_fahrenheit().value
            case 'celsius':
                quotient = self.value // other.to_celsius().value
            case 'kelvin':
                quotient = self.value // other.to_kelvin().value
        return Temperature(quotient, self.measurement)


    def __mod__(self, other):
        match self.measurement:
            case 'fahrenheit':
                quotient = self.value % other.to_fahrenheit().value
            case 'celsius':
                quotient = self.value % other.to_celsius().value
            case 'kelvin':
                quotient = self.value % other.to_kelvin().value
        return Temperature(quotient, self.measurement)


    def to_fahrenheit(self):
        '''Convert the temperature to Fahrenheit'''
        match self.measurement:
            case 'fahrenheit':
                return self
            case 'celsius':
                return Temperature((self.value * 9.0 / 5.0) + 32.0)
            case 'kelvin':
                return Temperature((self.value - 273.15) * (9.0 / 5.0) + 32)


    def to_celsius(self):
        '''Convert the temperature to Celsius'''
        measure = 'celsius'
        match self.measurement:
            case 'celsius':
                return self
            case 'fahrenheit':
                return Temperature(((self.value - 32.0) * 5.0 / 9.0), measure)
            case 'kelvin':
                return Temperature((self.value - 273.15), measure)


    def to_kelvin(self):
        '''Convert the temperature to Kelvin'''
        measure = 'kelvin'
        match self.measurement:
            case 'kelvin':
                return self
            case 'fahrenheit':
                return Temperature(((self.value - 32.0) * (5.0 / 9.0) + 273.15), measure)
            case 'celsius':
                return Temperature((self.value + 273.15), measure)


ABSOLUTE_ZERO = Temperature(0, measurement='kelvin')
FREEZING_POINT = Temperature(0, measurement='celsius')
BOILING_POINT = Temperature(100, measurement='celsius')
