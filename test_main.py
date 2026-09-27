import random
import pytest

from main import BigInt, DEFAULT_BASE

# 1
@pytest.mark.parametrize("value", [0, 1, -1, 42, -42, 10**50, -10**50])
def test_from_int(value):
    assert str(BigInt(value)) == str(value)

# 2 неподходящее основание
def test_bad_base():
    with pytest.raises(ValueError):
        BigInt(0, base=1)
    with pytest.raises(ValueError):
        BigInt(0, base=0)
    with pytest.raises(ValueError):
        BigInt(0, base=-5)

# 3 проверка числа со списка
def test_from_list():
    assert str(BigInt([4, 3, 2, 1])) == "1234"
    assert str(BigInt([0, 0, 1])) == "100"
    assert str(BigInt([0])) == "0"
    assert str(BigInt([0, 0, 0])) == "0"

# 4 неподходящий тип
def test_bad_type():
    with pytest.raises(TypeError):
        BigInt(3.14)
    with pytest.raises(TypeError):
        BigInt(None)

# 5 (+)
@pytest.mark.parametrize("a, b", [
    (0, 0),
    (1, 2), (-1, 2), (1, -2), (-1, -2),
    (5, -5), (-5, 5),
    (12345, 67890), (-12345, 67890), (12345, -67890), (-12345, -67890),
    (10**50, 10**30), (-10**50, 10**30),
    (999, 1), (999, 999),
])
def test_add(a, b):
    assert str(BigInt(a) + BigInt(b)) == str(a + b)

# 6 (-)
@pytest.mark.parametrize("a, b", [
    (0, 0), (5, 0), (0, 5), (5, 5),
    (5, 3), (3, 5), (-5, 3), (5, -3), (-5, -3),
    (10**50, 10**30), (10**30, 10**50),
    (-10**50, -10**30),
])
def test_sub(a, b):
    assert str(BigInt(a) - BigInt(b)) == str(a - b)

# 7 (*)
@pytest.mark.parametrize("a, b", [
    (0, 0), (0, 5), (5, 0),
    (1, 1), (1, -1), (-1, 1), (-1, -1),
    (123, 456), (-123, 456), (123, -456), (-123, -456),
    (10**30, 10**30), (-10**50, 10**20),
    (999999, 999999),
])
def test_mul(a, b):
    assert str(BigInt(a) * BigInt(b)) == str(a * b)

# 8 (//)
@pytest.mark.parametrize("a, b", [
    (10, 3), (100, 7), (10**30, 10**10),
    (-10, 3), (10, -3), (-10, -3),
    (12345, 67), (10**50, 7),
    (0, 5), (5, 10), (-5, 10), (5, -10),
    (1, 1), (-1, -1),
])
def test_floordiv(a, b):
    assert str(BigInt(a) // BigInt(b)) == str(a // b)

# 9 деление на ноль
def test_zero_div():
    with pytest.raises(ZeroDivisionError):
        BigInt(5) // BigInt(0)
    with pytest.raises(ZeroDivisionError):
        BigInt(0) // BigInt(0)

# 10 разные основания
@pytest.mark.parametrize("base", [2, 3, 8, 10, 16, 100, 1000, 10**6, 10**9])
def test_various_bases(base):
    a, b = 123456, 789
    A = BigInt(a, base=base)
    B = BigInt(b, base=base)
    assert str(A + B) == str(a + b)
    assert str(A - B) == str(a - b)
    assert str(A * B) == str(a * b)
    assert str(A // B) == str(a // b)

# 11 разные основания при разных знаках у чисел
@pytest.mark.parametrize("base", [2, 7, 10, 256])
def test_bases_with_negatives(base):
    a, b = -1234, 56
    A = BigInt(a, base=base)
    B = BigInt(b, base=base)
    assert str(A + B) == str(a + b)
    assert str(A - B) == str(a - b)
    assert str(A * B) == str(a * b)
    assert str(A // B) == str(a // b)

# 12 сравнение
def test_comparisons():
    assert BigInt(-5) < BigInt(3)
    assert BigInt(3) > BigInt(-5)
    assert BigInt(5) == BigInt(5)
    assert BigInt(-5) <= BigInt(-5)
    assert BigInt(-5) >= BigInt(-5)
    assert BigInt(-5) != BigInt(5)
    assert BigInt(3) < BigInt(5)
    assert BigInt(-5) < BigInt(-3)
    assert BigInt(-3) > BigInt(-5)
    assert BigInt(0) == BigInt(0)
    assert BigInt(0) != BigInt(1)

# 13 проверка унарного минуса
def test_neg():
    assert str(-BigInt(5)) == "-5"
    assert str(-BigInt(-5)) == "5"
    assert str(-BigInt(0)) == "0"

# 14 проверка работы модуля
def test_abs():
    assert str(abs(BigInt(-5))) == "5"
    assert str(abs(BigInt(5))) == "5"
    assert str(abs(BigInt(0))) == "0"

