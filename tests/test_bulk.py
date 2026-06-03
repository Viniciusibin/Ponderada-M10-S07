"""Bulk parametrized tests — variação #5: aumento artificial de testes."""
import pytest
from calculator import add, subtract, multiply, divide, power


@pytest.mark.parametrize("a,b,expected", [
    (0, 0, 0), (1, 1, 2), (2, 3, 5), (10, 20, 30), (100, 200, 300),
    (-1, 1, 0), (-5, -5, -10), (7, 8, 15), (99, 1, 100), (50, 50, 100),
])
def test_add_bulk(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [
    (10, 5, 5), (20, 10, 10), (100, 1, 99), (0, 0, 0), (50, 25, 25),
    (-1, -1, 0), (1000, 999, 1), (3, 3, 0), (7, 2, 5), (8, 4, 4),
])
def test_subtract_bulk(a, b, expected):
    assert subtract(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [
    (0, 5, 0), (1, 1, 1), (2, 3, 6), (10, 10, 100), (5, 4, 20),
    (-1, 1, -1), (-2, -2, 4), (3, 7, 21), (6, 6, 36), (9, 9, 81),
])
def test_multiply_bulk(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [
    (10, 2, 5.0), (20, 4, 5.0), (100, 10, 10.0), (9, 3, 3.0), (8, 2, 4.0),
    (1, 1, 1.0), (6, 2, 3.0), (15, 5, 3.0), (50, 10, 5.0), (81, 9, 9.0),
])
def test_divide_bulk(a, b, expected):
    assert divide(a, b) == expected


@pytest.mark.parametrize("base,exp,expected", [
    (2, 0, 1), (2, 1, 2), (2, 2, 4), (2, 3, 8), (2, 4, 16),
    (3, 2, 9), (4, 2, 16), (5, 2, 25), (10, 2, 100), (1, 100, 1),
])
def test_power_bulk(base, exp, expected):
    assert power(base, exp) == expected
