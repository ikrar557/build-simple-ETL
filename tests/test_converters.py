import pytest
from utils.transform.converters import convert_price_to_idr, clean_string, parse_colors, parse_rating

def test_convert_price_to_idr():
    assert convert_price_to_idr(10.0) == 160000.0
    assert convert_price_to_idr('10.0') == 160000.0
    assert convert_price_to_idr(0) == 0.0
    assert convert_price_to_idr('invalid') == 0.0
    assert convert_price_to_idr(None) == 0.0
    assert convert_price_to_idr(complex(1, 2)) == 0.0

def test_convert_price_to_idr_rate_validation():
    assert convert_price_to_idr(10.0, rate=0) == 0.0
    assert convert_price_to_idr(10.0, rate=-1) == 0.0
    assert convert_price_to_idr(10.0, rate='invalid') == 0.0
    assert convert_price_to_idr(10.0, rate=None) == 0.0
    
    assert convert_price_to_idr(10.0, rate=15000) == 150000.0
    assert convert_price_to_idr(10.0, rate=1.5) == 15.0

def test_clean_string():
    assert clean_string('  test  ') == 'test'
    assert clean_string('') == ''
    assert clean_string(None) == 'None'
    assert clean_string(123) == '123'
    assert clean_string(['not a string']) == str(['not a string'])

    assert clean_string(True) == 'True'
    assert clean_string(False) == 'False'
    assert clean_string(0) == '0'
    
    assert clean_string('\n test \t') == 'test'
    assert clean_string('   ') == ''

def test_clean_string_error_handling():
    class NoStrMethod:
        def __str__(self):
            raise AttributeError("No str method")
    
    assert clean_string(NoStrMethod()) == ''
    
    class BadStrMethod:
        def __str__(self):
            raise TypeError("Bad str conversion")
    
    assert clean_string(BadStrMethod()) == ''
    
    class NoStripMethod:
        def __str__(self):
            return "test"
        def strip(self, *args):
            raise TypeError("strip() takes no arguments")
    
    assert clean_string(NoStripMethod()) == 'test'

def test_parse_colors():
    assert parse_colors('3 colors') == 3
    assert parse_colors('3') == 3
    assert parse_colors(3) == 3
    assert parse_colors('invalid') == 0
    assert parse_colors('') == 0
    assert parse_colors(None) == 0

def test_parse_rating():
    assert parse_rating(4.5) == 4.5
    assert parse_rating('4.5') == 4.5
    assert parse_rating(5) == 5.0
    assert parse_rating('invalid') == 0.0
    assert parse_rating(None) == 0.0
    assert parse_rating('') == 0.0