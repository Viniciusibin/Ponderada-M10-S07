"""Simple calculator module for CI/CD pipeline experiment."""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base, exp):
    return base ** exp


def modulo(a, b):
    if b == 0:
        raise ValueError("Cannot modulo by zero")
    return a % b


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def factorial(n):
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def fibonacci(n):
    if n < 0:
        raise ValueError("Fibonacci not defined for negative numbers")
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))


def percentage(part, total):
    if total == 0:
        raise ValueError("Total cannot be zero")
    return (part / total) * 100
