"""Slow test — variação #6: simula teste com alta latência."""
import time
from calculator import add


def test_slow_operation():
    """Simula operação lenta de integração (sleep proposital)."""
    time.sleep(10)
    assert add(1, 1) == 2
