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
        if self.digits == [0]:
            self.sign = 1

    def _cmp_abs(self, other):
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

    def __neg__(self):
        """Унарный минус: меняет знак, кроме нуля."""
        r = self._copy()
        if r.digits != [0]:
            r.sign = -r.sign
        return r

    def __abs__(self):
        """Модуль числа."""
        r = self._copy()
        r.sign = 1
        return r

    def _add_abs(self, other):
        """|self| + |other| в столбик с переносом."""
        base = self.base
        result = []
        carry = 0
        n = max(len(self.digits), len(other.digits))
        for i in range(n):
            s = carry
            if i < len(self.digits):
                s += self.digits[i]
            if i < len(other.digits):
                s += other.digits[i]
            result.append(s % base)
            carry = s // base
        if carry:
            result.append(carry)
        r = BigInt(0, base)
        r.digits = result
        r.sign = 1
        r._normalize()
        return r
    
    def _sub_abs(self, other):
        """|self| - |other| при условии |self| >= |other|."""
        base = self.base
        result = []
        borrow = 0
        for i in range(len(self.digits)):
            d = self.digits[i] - borrow
            if i < len(other.digits):
                d -= other.digits[i]
            if d < 0:
                d += base
                borrow = 1
            else:
                borrow = 0
            result.append(d)
        r = BigInt(0, base)
        r.digits = result
        r.sign = 1
        r._normalize()
        return r

    def __add__(self, other):
        """Сложение: одинаковые знаки - складываем модули, разные - вычитаем меньший из большего."""
        if not isinstance(other, BigInt):
            other = BigInt(other, self.base)
        if self.sign == other.sign:
            r = self._add_abs(other)
            r.sign = self.sign
            r._normalize()
            return r
        c = self._cmp_abs(other)
        if c == 0:
            return BigInt(0, self.base)
        if c > 0:
            r = self._sub_abs(other)
            r.sign = self.sign
        else: # c < 0
            r = other._sub_abs(self)
            r.sign = other.sign
        r._normalize()
        return r

    def __sub__(self, other):
        """Вычитание: self + (-other)."""
        if not isinstance(other, BigInt):
            other = BigInt(other, self.base)
        return self + (-other)

    def __mul__(self, other):
        """Умножение: O(n·m)."""
        if not isinstance(other, BigInt):
            other = BigInt(other, self.base)
        base = self.base
        result = [0] * (len(self.digits) + len(other.digits))
        for i, da in enumerate(self.digits):
            carry = 0
            for j, db in enumerate(other.digits):
                cur = result[i + j] + da * db + carry
                result[i + j] = cur % base
                carry = cur // base
            k = i + len(other.digits)
            while carry:
                cur = result[k] + carry
                result[k] = cur % base
                carry = cur // base
                k += 1
        r = BigInt(0, base)
        r.digits = result
        r.sign = self.sign * other.sign
        r._normalize()
        return r

    def _divmod_abs(self, other):
        """|self| // |other| - функция для целочисленного деления (вспомогательная)"""
        base = self.base
        if other.digits == [0]:
            raise ZeroDivisionError("Деление на ноль")
        if self._cmp_abs(other) < 0:
            return BigInt(0, base), self._copy()

        a = self.digits
        quotient = [0] * len(a)
        remainder = BigInt(0, base)

        for i in range(len(a) - 1, -1, -1):
            remainder.digits.insert(0, a[i])
            remainder._normalize()

            lo, hi = 0, base - 1
            best = 0
            while lo <= hi:
                mid = (lo + hi) // 2
                trial = other * BigInt(mid, base)
                if trial._cmp_abs(remainder) <= 0:
                    best = mid
                    lo = mid + 1
                else:
                    hi = mid - 1

            quotient[i] = best
            if best:
                remainder = remainder._sub_abs(other * BigInt(best, base))

        q = BigInt(0, base)
        q.digits = quotient
        q.sign = 1
        q._normalize()
        return q, remainder

    def __floordiv__(self, other):
        """Целочисленное деление."""
        if not isinstance(other, BigInt):
            other = BigInt(other, self.base)
        q, _ = self._divmod_abs(other)
        q.sign = self.sign * other.sign
        if q.digits == [0]:
            q.sign = 1
        return q

    def __str__(self):
        """Строковое представление в десятичной системе."""
        if self.digits == [0]:
            return "0"
        n = 0
        for d in reversed(self.digits):
            n = n * self.base + d
        return ("-" if self.sign < 0 else "") + str(n)