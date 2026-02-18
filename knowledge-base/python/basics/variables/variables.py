# =============================================================================
# Тема: Переменные
# Раздел: python/basics
# Документация: variables.md
# =============================================================================

# --- Пример 1: Переменная — это ссылка, не контейнер ---
# В Python переменная хранит не значение, а адрес объекта в памяти.
# b = a не копирует список — оба имени указывают на один объект.

a = [1, 2, 3]
b = a
b.append(4)

print(a)        # [1, 2, 3, 4] — изменился через b!
print(a is b)   # True — один и тот же объект

# Независимая копия через .copy()
c = a.copy()
c.append(99)
print(a)        # [1, 2, 3, 4] — не изменился
print(a is c)   # False — разные объекты


# --- Пример 2: Динамическая типизация ---
# Тип определяется значением. Неявного приведения типов нет.

x = 42
print(type(x))                       # <class 'int'>

x = "hello"
print(type(x))                       # <class 'str'>

x = [1, 2, 3]
print(isinstance(x, list))           # True
print(isinstance(x, (list, tuple)))  # True — несколько типов сразу


# --- Пример 3: LEGB — поиск имени по уровням ---
# Python ищет: Local → Enclosing → Global → Built-in

value = "global"

def outer():
    value = "enclosing"

    def inner():
        value = "local"
        print(value)    # "local"

    inner()
    print(value)        # "enclosing"

outer()
print(value)            # "global"


# --- Пример 4: global — изменение переменной уровня модуля ---
# Без global Python создаёт локальную переменную и выбрасывает UnboundLocalError.

counter = 0

def increment():
    global counter
    counter += 1

increment()
increment()
print(counter)   # 2


# --- Пример 5: nonlocal — замыкание с сохранением состояния ---
# nonlocal позволяет изменять переменную объемлющей функции.
# Основа паттерна stateful-замыкания.

def make_counter(start: int = 0):
    count = start

    def tick() -> int:
        nonlocal count
        count += 1
        return count

    return tick

counter = make_counter(10)
print(counter())   # 11
print(counter())   # 12
print(counter())   # 13


# --- Пример 6: Распаковка и расширенная распаковка ---
# Параллельное присваивание: правая часть вычисляется целиком, затем распаковывается.

a, b = 10, 20
a, b = b, a                     # swap без temp-переменной
print(a, b)                     # 20 10

first, *rest = [1, 2, 3, 4, 5]
print(first, rest)              # 1 [2, 3, 4, 5]

*init, last = [1, 2, 3, 4, 5]
print(init, last)               # [1, 2, 3, 4] 5

head, *middle, tail = [1, 2, 3, 4, 5]
print(head, middle, tail)       # 1 [2, 3, 4] 5

only, *empty = [42]
print(only, empty)              # 42 []


# --- Пример 7: == vs is — равенство vs идентичность ---
# == сравнивает значения (__eq__), is проверяет — один ли объект в памяти.

a = [1, 2, 3]
b = [1, 2, 3]   # новый объект
c = a           # тот же объект

print(a == b)   # True  — значения равны
print(a is b)   # False — разные объекты
print(a is c)   # True  — один объект

# is правильно использовать только для None, True, False:
value = None
if value is None:
    print("value is None")


# --- Пример 8: shallow copy vs deep copy ---
# .copy() копирует только верхний уровень. Вложенные объекты — по-прежнему ссылки.

import copy

original = {"name": "Alice", "scores": [10, 20, 30]}
shallow  = original.copy()
deep     = copy.deepcopy(original)

shallow["scores"].append(99)
print(original["scores"])   # [10, 20, 30, 99] — shallow не защитил вложенный список
print(deep["scores"])       # [10, 20, 30]     — deepcopy защитил
