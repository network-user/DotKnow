# =============================================================================
# Тема: Функции
# Раздел: python/basics
# Документация: functions.md
# =============================================================================

# --- Пример 1: Функция — объект первого класса ---
# Функцию можно присвоить переменной, передать как аргумент,
# положить в список — это полноценный объект.

def greet(name: str) -> str:
    return f"Привет, {name}!"

say_hi = greet                          # без скобок — передаём объект функции
print(say_hi("Alice"))                  # Привет, Alice!
print(type(say_hi))                     # <class 'function'>

operations = [str.upper, str.strip, str.title]
for op in operations:
    print(repr(op("  hello world  ")))


# --- Пример 2: Все виды параметров в одной функции ---
# Порядок: pos_only (/) → normal → *args → kw_only → **kwargs

def full_demo(
    pos_only: int,          # только позиционный — нельзя передать по имени
    /,
    normal: str,            # обычный — позиционный или ключевой
    *args: float,           # произвольные позиционные → tuple
    kw_only: bool = False,  # только ключевой
    **kwargs: str,          # произвольные ключевые → dict
) -> None:
    print(f"pos_only : {pos_only}")
    print(f"normal   : {normal!r}")
    print(f"args     : {args}")
    print(f"kw_only  : {kw_only}")
    print(f"kwargs   : {kwargs}")

full_demo(1, "hi", 2.5, 3.5, kw_only=True, color="red", size="L")


# --- Пример 3: Опасный дефолтный аргумент ---
# Изменяемый дефолт создаётся ОДИН РАЗ при объявлении функции.
# Все вызовы без явного аргумента разделяют один объект.

def bad_log(msg: str, history: list = []) -> list:
    history.append(msg)
    return history

print(bad_log("first"))    # ['first']
print(bad_log("second"))   # ['first', 'second'] — накопилось!

# Правильно: None как sentinel-значение
def good_log(msg: str, history: list | None = None) -> list:
    if history is None:
        history = []        # новый список при каждом вызове
    history.append(msg)
    return history

print(good_log("first"))   # ['first']
print(good_log("second"))  # ['second'] — независимый список


# --- Пример 4: Функция высшего порядка — принимает функцию ---
from collections.abc import Callable

def apply_to_all(func: Callable[[int], int], items: list[int]) -> list[int]:
    return [func(x) for x in items]

print(apply_to_all(lambda x: x ** 2, [1, 2, 3, 4]))    # [1, 4, 9, 16]
print(apply_to_all(abs, [-3, -1, 0, 2, -5]))            # [3, 1, 0, 2, 5]


# --- Пример 5: Фабрика функций — замыкание ---
# Внутренняя функция «помнит» переменные из объемлющей области (closure).

def make_multiplier(factor: int) -> Callable[[int], int]:
    def multiply(x: int) -> int:
        return x * factor    # factor захвачен из make_multiplier
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))                            # 10
print(triple(5))                            # 15
print([double(i) for i in range(1, 6)])     # [2, 4, 6, 8, 10]


# --- Пример 6: Lambda в реальных задачах ---

students = [
    {"name": "Charlie", "grade": 75, "age": 22},
    {"name": "Alice",   "grade": 92, "age": 20},
    {"name": "Bob",     "grade": 85, "age": 21},
]

# Сортировка по оценке (по убыванию)
by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)
print([s["name"] for s in by_grade])    # ['Alice', 'Bob', 'Charlie']

# Фильтрация — только отличники
excellent = list(filter(lambda s: s["grade"] >= 90, students))
print([s["name"] for s in excellent])   # ['Alice']

# map — извлечь имена
names = list(map(lambda s: s["name"], students))
print(names)                            # ['Charlie', 'Alice', 'Bob']


# --- Пример 7: Docstring + валидация + raises ---

def divide(dividend: float, divisor: float) -> float:
    """
    Делит одно число на другое.

    Args:
        dividend: Делимое.
        divisor: Делитель. Не должен быть равен нулю.

    Returns:
        Результат деления в виде float.

    Raises:
        ZeroDivisionError: Если divisor равен нулю.

    Example:
        >>> divide(10, 4)
        2.5
    """
    if divisor == 0:
        raise ZeroDivisionError("Делитель не может быть равен нулю")
    return dividend / divisor

print(divide(10, 4))   # 2.5

try:
    divide(5, 0)
except ZeroDivisionError as e:
    print(e)           # Делитель не может быть равен нулю


# --- Пример 8: Рекурсия — factorial и fibonacci ---

def factorial(n: int) -> int:
    """n! рекурсивно. Базовый случай: n <= 1 -> return 1."""
    if n < 0:
        raise ValueError("n >= 0")
    if n <= 1:                    # базовый случай — без него RecursionError
        return 1
    return n * factorial(n - 1)  # рекурсивный вызов

def fibonacci(n: int) -> int:
    """n-е число Фибоначчи (наглядно, но неэффективно — O(2^n))."""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

print(factorial(6))                          # 720
print(fibonacci(10))                         # 55
print([fibonacci(i) for i in range(8)])      # [0, 1, 1, 2, 3, 5, 8, 13]


# --- Пример 9: Частые ошибки ---

# Ошибка 1: забытый return
def broken_sum(a: int, b: int):
    result = a + b
    # return result  ← закомментировано намеренно

x = broken_sum(3, 4)
print(x)          # None
# print(x + 1)    # TypeError — раскомментируй, чтобы увидеть

# Ошибка 2: изменение переданного списка
def pop_first(lst: list) -> None:
    lst.pop(0)    # изменяет оригинал!

data = [10, 20, 30]
pop_first(data)
print(data)       # [20, 30] — оригинал изменился

# Безопасный вариант
data = [10, 20, 30]
pop_first(data.copy())
print(data)       # [10, 20, 30] — оригинал цел
