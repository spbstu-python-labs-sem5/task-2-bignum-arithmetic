"""Задача №2. Длинная арифметика для целых чисел."""

DEFAULT_BASE = 10

class BigInt:
    """Целое число произвольной длины в системе счисления по основанию base."""
    def __init__(self, value=0, base=DEFAULT_BASE):
        if base < 2:
            raise ValueError("Нужно base >= 2")
        self.base = base
        self.sign = 1
        self.digits = [0]

        if isinstance(value, int):
            self._from_int(value)
        elif isinstance(value, str):
            self._from_string(value)
        elif isinstance(value, (list, tuple)):
            self.digits = [int(d) for d in value]
            self._normalize()
        else:
            raise TypeError(f"unsupported type: {type(value).__name__}")
