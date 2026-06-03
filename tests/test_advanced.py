"""Advanced tests — used for variation commits (slow, bulk, etc.)."""
from calculator import add, multiply, is_prime, fibonacci


class TestBulkOperations:
    """Placeholder for bulk tests added in later variations."""

    def test_add_sequence(self):
        results = [add(i, i + 1) for i in range(10)]
        assert results == [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

    def test_multiply_sequence(self):
        results = [multiply(i, 2) for i in range(5)]
        assert results == [0, 2, 4, 6, 8]

    def test_primes_up_to_20(self):
        primes = [n for n in range(2, 21) if is_prime(n)]
        assert primes == [2, 3, 5, 7, 11, 13, 17, 19]

    def test_fibonacci_sequence(self):
        seq = [fibonacci(i) for i in range(8)]
        assert seq == [0, 1, 1, 2, 3, 5, 8, 13]
