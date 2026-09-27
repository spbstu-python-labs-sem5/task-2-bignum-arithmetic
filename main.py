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
        """Парсит строку вида '-123' в число (через накопление *10 + цифра)."""
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

    def _copy(self):
        """Возвращает копию числа."""
        r = BigInt(0, self.base)
        r.sign = self.sign
        r.digits = self.digits[:]
        return r
    
    def _normalize(self):
        """Убирает ведущие нули, к примеру: [0, 1, 0, 0] -> [0, 1], а также у нуля принудительно ставит знак +1."""
        while len(self.digits) > 1 and self.digits[-1] == 0:
            self.digits.pop()
        if self.digits == [0]
            self.sign = 1

    def _cmp_abs(self, second):
        """Сравнивает модули: -1 / 0 / 1."""
        if len(self.digits) != len(other.digits):
            if len(self.digits) > len(other.digits):
                return 1
            return -1
    
        for i in range(len(self.digits) - 1, -1, -1):
        if self.digits[i] != other.digits[i]:
            if self.digits[i] > other.digits[i]:
                return 1
            return -1

        return 0

        def __eq__(self, other):
        """Равенство: когда совпадают знак и цифры."""
        if not isinstance(other, BigInt):
            other = BigInt(other, self.base)
        return self.sign == other.sign and self.digits == other.digits

            def __lt__(self, other):
        """Меньше: сначала по знаку, потом по модулю."""
        if not isinstance(other, BigInt):
            other = BigInt(other, self.base)
        if self.sign != other.sign:
            return self.sign < other.sign
        c = self._cmp_abs(other)
        return c < 0 if self.sign > 0 else c > 0

        def __le__(self, other):
            """Меньше или равно."""
            return self < other or self == other

        def __gt__(self, other):
            """Больше. Используем уже написанный __le__."""
            return not self <= other

        def __ge__(self, other):
            """Больше или равно. Используем уже написанный __le__."""
            return not self < other