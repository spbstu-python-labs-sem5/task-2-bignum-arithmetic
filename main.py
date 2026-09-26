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
            raise TypeError(f"Неподдерживаемый тип: {type(value).__name__}")

    def _from_int(self, n):
        self.sign = 1 if n >= 0 else -1
        n = abs(n)
        self.digits = []
        if n == 0:
            self.digits = [0]
            return
        while n > 0:
            self.digits.append(n % self.base)
            n //= self.base

    def _from_string(self, s):
        s = s.strip()
        if not s:
            raise ValueError("Пустая строка")
        sign = 1
        if s[0] == '-':
            sign, s = -1, s[1:]
        elif s[0] == '+':
            s = s[1:]
        if not s:
            raise ValueError("Строка не содержит цифр")
        value = BigInt(0, self.base)
        ten = BigInt(10, self.base)
        for ch in s:
            if not ch.isdigit(): raise ValueError(f"Недопустимый символ: {ch!r}")
            value = value * ten + BigInt(int(ch), self.base)
        self.digits = value.digits[:]
        self.sign = sign if self.digits != [0] else 1
