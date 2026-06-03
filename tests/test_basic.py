"""Basic tests for calculator module — baseline variation."""
import pytest
from calculator import (
    add, subtract, multiply, divide,
    power, modulo, is_prime, factorial,
    fibonacci, gcd, lcm, clamp, percentage,
)


class TestAdd:
    def test_positive(self):
        assert add(2, 3) == 5

    def test_negative(self):
        assert add(-1, -2) == -3

    def test_zero(self):
        assert add(0, 0) == 0

    def test_mixed(self):
        assert add(-5, 10) == 5


class TestSubtract:
    def test_positive(self):
        assert subtract(10, 3) == 7

    def test_negative_result(self):
        assert subtract(3, 10) == -7

    def test_zero(self):
        assert subtract(5, 5) == 0


class TestMultiply:
    def test_positive(self):
        assert multiply(3, 4) == 12

    def test_by_zero(self):
        assert multiply(100, 0) == 0

    def test_negative(self):
        assert multiply(-3, 4) == -12

    def test_both_negative(self):
        assert multiply(-3, -4) == 12


class TestDivide:
    def test_positive(self):
        assert divide(10, 2) == 5

    def test_float(self):
        assert divide(7, 2) == 3.5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError):
            divide(10, 0)

    def test_negative(self):
        assert divide(-10, 2) == -5


class TestPower:
    def test_square(self):
        assert power(3, 2) == 9

    def test_zero_exp(self):
        assert power(5, 0) == 1

    def test_one_base(self):
        assert power(1, 100) == 1


class TestModulo:
    def test_basic(self):
        assert modulo(10, 3) == 1

    def test_even(self):
        assert modulo(10, 2) == 0

    def test_by_zero(self):
        with pytest.raises(ValueError):
            modulo(10, 0)


class TestIsPrime:
    def test_two_is_prime(self):
        assert is_prime(2) is True

    def test_one_is_not_prime(self):
        assert is_prime(1) is False

    def test_large_prime(self):
        assert is_prime(97) is True

    def test_composite(self):
        assert is_prime(4) is False

    def test_zero(self):
        assert is_prime(0) is False


class TestFactorial:
    def test_zero(self):
        assert factorial(0) == 1

    def test_one(self):
        assert factorial(1) == 1

    def test_five(self):
        assert factorial(5) == 120

    def test_negative(self):
        with pytest.raises(ValueError):
            factorial(-1)


class TestFibonacci:
    def test_zero(self):
        assert fibonacci(0) == 0

    def test_one(self):
        assert fibonacci(1) == 1

    def test_ten(self):
        assert fibonacci(10) == 55

    def test_negative(self):
        with pytest.raises(ValueError):
            fibonacci(-1)


class TestGcd:
    def test_basic(self):
        assert gcd(12, 8) == 4

    def test_coprime(self):
        assert gcd(7, 13) == 1

    def test_same(self):
        assert gcd(5, 5) == 5


class TestLcm:
    def test_basic(self):
        assert lcm(4, 6) == 12

    def test_coprime(self):
        assert lcm(3, 7) == 21


class TestClamp:
    def test_in_range(self):
        assert clamp(5, 0, 10) == 5

    def test_below_min(self):
        assert clamp(-5, 0, 10) == 0

    def test_above_max(self):
        assert clamp(15, 0, 10) == 10


class TestPercentage:
    def test_half(self):
        assert percentage(50, 100) == 50.0

    def test_quarter(self):
        assert percentage(25, 100) == 25.0

    def test_zero_total(self):
        with pytest.raises(ValueError):
            percentage(10, 0)
