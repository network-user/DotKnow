# --- Пример 1: Базовое использование ---
# Создание списка квадратов чисел от 0 до 4
numbers = range(5)
squares = [n * n for n in numbers]
print(f"Квадраты чисел: {squares}")

# --- Пример 2: Фильтрация с условием if ---
# Создание списка только четных чисел из диапазона от 0 до 9
all_numbers = range(10)
even_numbers = [n for n in all_numbers if n % 2 == 0]
print(f"Четные числа: {even_numbers}")

# --- Пример 3: Условное выражение (if-else) ---
# Замена нечетных чисел на строку 'odd', четные остаются как есть
mixed_list = [n if n % 2 == 0 else 'odd' for n in range(5)]
print(f"Список с 'odd': {mixed_list}")

# --- Пример 4: Вложенные списковые включения ---
# Создание плоского списка из списка списков
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat_list = [num for row in matrix for num in row]
print(f"Плоский список: {flat_list}")

# --- Пример 5: Комбинация if и вложенных циклов ---
# Создание списка пар (x, y) где x < y
coords = [(x, y) for x in range(3) for y in range(3) if x < y]
print(f"Координаты (x < y): {coords}")

# --- Пример 6: find_the_bug - Неправильное расположение if-else ---
# Цель: получить список, где числа > 5 заменены на 'large', иначе число
# Ошибка: if-else стоит после for, что неверно для условного выражения
buggy_list_comprehension = [
    n for n in range(10) if n > 5 else 'large'
]
# Ожидаемая ошибка: SyntaxError
# Правильно: [n if n <= 5 else 'large' for n in range(10)]

# --- Пример 7: fill_the_gap - Заполнить пропущенное условие ---
# Задание: Создать список только положительных чисел из данного списка
numbers_with_negatives = [-2, -1, 0, 1, 2, 3]
# positive_numbers = [n for n in numbers_with_negatives ___ n > 0]
# Ожидаемый результат: [1, 2, 3]
# Пропущенное слово: if
