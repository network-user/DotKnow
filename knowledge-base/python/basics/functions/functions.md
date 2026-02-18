---
title: "Функции"
difficulty: easy
tags: [functions, args, kwargs, annotations, lambda, closures, recursion, docstring]
added: "2026-02-18"
last_reviewed: null
---

## Что это такое

Функция — это именованный блок кода, который принимает данные на вход,
выполняет работу и возвращает результат.

В Python функции являются **объектами первого класса** (first-class objects).
Это значит, что функция — такой же объект, как число или строка: её можно
присвоить переменной, передать как аргумент, вернуть из функции, положить в список.

```python
def greet(name: str) -> str:
    return f"Привет, {name}!"

say_hi = greet              # присваиваем функцию переменной (без скобок!)
print(say_hi("Alice"))      # Привет, Alice!

funcs = [str.upper, str.strip, str.title]
for f in funcs:
    print(f("  hello world  "))
```

---

## Анатомия функции

```
def имя_функции(параметры) -> тип_возвращаемого:
    """Docstring."""
    # тело
    return значение
```

- `def` — ключевое слово объявления функции
- `имя_функции` — `snake_case` по PEP 8
- `-> тип` — аннотация возвращаемого типа (не обязательна, но рекомендуется)
- `return` — возвращает значение; если `return` нет — функция вернёт `None`
- `docstring` — строка документации; доступна через `help(func)` и `func.__doc__`

---

## Виды параметров

Порядок объявления строго зафиксирован:

```
def f(позиционный_только, /, обычный, *args, только_ключевой, **kwargs):
```

| Вид | Синтаксис | Тип внутри | Описание |
|-----|-----------|------------|----------|
| Позиционный-только | `def f(x, /)` | значение | Нельзя передать по имени |
| Обычный | `def f(x)` | значение | Позиционный или ключевой |
| С дефолтом | `def f(x=10)` | значение | Необязательный |
| `*args` | `def f(*args)` | `tuple` | Произвольное кол-во позиционных |
| `**kwargs` | `def f(**kwargs)` | `dict` | Произвольное кол-во ключевых |
| Только ключевой | `def f(*, x)` | значение | Только по имени, после `*` |

```python
def create_report(
    title: str,
    /,
    *sections: str,
    author: str = "Unknown",
    **metadata: str,
) -> dict:
    return {"title": title, "sections": sections, "author": author, **metadata}

report = create_report(
    "Python Guide",
    "Variables", "Functions",
    author="Alice",
    version="1.0",
)
```

---

## Аннотации типов (Python 3.12+)

Аннотации — подсказки для IDE и линтеров. На выполнение не влияют.

```python
from collections.abc import Callable

def process(items: list[int], *, reverse: bool = False) -> list[int]:
    return sorted(items, reverse=reverse)

# Python 3.12 — новый синтаксис type alias
type Matrix = list[list[float]]

# Обобщённые функции через TypeVar
def filter_items[T](items: list[T], pred: Callable[[T], bool]) -> list[T]:
    return [x for x in items if pred(x)]

evens = filter_items([1, 2, 3, 4, 5], lambda x: x % 2 == 0)
print(evens)   # [2, 4]
```

---

## Опасный дефолтный аргумент

Дефолтные значения вычисляются **один раз** — при объявлении функции, не при вызове.
Если дефолт — изменяемый объект (`list`, `dict`, `set`), он накапливает данные между вызовами.

```python
# ПЛОХО
def bad_append(value: int, storage: list = []) -> list:
    storage.append(value)
    return storage

print(bad_append(1))   # [1]
print(bad_append(2))   # [1, 2] — тот же список!
print(bad_append(3))   # [1, 2, 3]

# ХОРОШО — None как sentinel
def good_append(value: int, storage: list | None = None) -> list:
    if storage is None:
        storage = []    # новый список при каждом вызове
    storage.append(value)
    return storage

print(good_append(1))   # [1]
print(good_append(2))   # [2] — независимый список
```

---

## Функции высшего порядка

Функция высшего порядка принимает другую функцию как аргумент или возвращает функцию.

```python
from collections.abc import Callable

# Принимает функцию как аргумент
def apply_twice(func: Callable, value):
    return func(func(value))

print(apply_twice(lambda x: x * 2, 3))   # 12

# Фабрика функций — возвращает функцию
def make_power(exp: int):
    def power(base: int) -> int:
        return base ** exp   # exp захвачен из объемлющей области
    return power

square = make_power(2)
cube   = make_power(3)
print(square(4))   # 16
print(cube(3))     # 27
```

Встроенные функции высшего порядка: `map()`, `filter()`, `sorted()`, `max()`, `min()`.

---

## Lambda-функции

Lambda — анонимная функция в одно выражение. Используй только для простых операций.

```python
# lambda параметры: выражение
double = lambda x: x * 2
print(double(5))   # 10

# Основное применение — key-функция
students = [
    {"name": "Bob",   "grade": 85},
    {"name": "Alice", "grade": 92},
    {"name": "Carol", "grade": 78},
]

by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)
print(by_grade[0]["name"])   # Alice

# filter и map
numbers = [1, 2, 3, 4, 5, 6]
evens   = list(filter(lambda x: x % 2 == 0, numbers))   # [2, 4, 6]
squared = list(map(lambda x: x ** 2, numbers))           # [1, 4, 9, 16, 25, 36]
```

> Если лямбда становится сложной или используется в нескольких местах — замени обычной функцией.

---

## Docstring: документирование функций

Docstring пишется сразу после `def` как первая строка тела. Формат — **Google Style**.

```python
def divide(dividend: float, divisor: float) -> float:
    """
    Делит одно число на другое.

    Args:
        dividend: Делимое.
        divisor: Делитель. Не должен быть равен нулю.

    Returns:
        Результат деления.

    Raises:
        ZeroDivisionError: Если divisor равен нулю.

    Example:
        >>> divide(10, 4)
        2.5
    """
    if divisor == 0:
        raise ZeroDivisionError("Делитель не может быть равен нулю")
    return dividend / divisor
```

---

## Рекурсия

Рекурсия — вызов функцией самой себя. Обязательно нужен **базовый случай** (условие выхода),
иначе получим `RecursionError`. Лимит CPython по умолчанию — 1000 вызовов.

```python
def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n должно быть >= 0")
    if n <= 1:              # базовый случай
        return 1
    return n * factorial(n - 1)

# factorial(5) -> 5 * 4 * 3 * 2 * 1 = 120
print(factorial(5))   # 120
print(factorial(0))   # 1
```

---

## Частые ошибки

**1. Забытый `return` — функция возвращает `None`:**
```python
def multiply(a, b):
    result = a * b
    # return result  ← забыли!

x = multiply(3, 4)
print(x)        # None
print(x + 1)    # TypeError: unsupported operand type(s): NoneType + int
```

**2. Изменяемый дефолтный аргумент** — см. раздел выше.

**3. Изменение переданного списка внутри функции:**
```python
def pop_first(lst: list) -> None:
    lst.pop(0)     # изменяет оригинал!

data = [1, 2, 3]
pop_first(data)
print(data)   # [2, 3] — оригинал уничтожен

# Безопасно — передавать копию:
pop_first(data.copy())
```

**4. Рекурсия без базового случая:**
```python
def infinite(n):
    return infinite(n - 1)   # RecursionError: maximum recursion depth exceeded
```

---

## Вопросы для самопроверки

- Что вернёт функция, в которой нет `return`?
- Почему нельзя использовать `[]` как дефолтный аргумент? Как исправить?
- Чем `*args` отличается от `**kwargs`? Какой тип данных они образуют внутри функции?
- В чём разница между `def f(x)` и `def f(*, x)`?
- Что такое функция высшего порядка? Назови три встроенных примера из Python.
- Когда стоит использовать `lambda`, а когда лучше обычная функция?
- Что произойдёт с оригинальным списком, если вызвать `.append()` внутри функции?
- Какой лимит рекурсии в CPython по умолчанию и как его изменить?
