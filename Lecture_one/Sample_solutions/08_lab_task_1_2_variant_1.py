"""Лабораторна 1, завдання 1.2, демонстраційний варіант 1.

Табулювання кусочно заданої функції на [0, 1] з кроком 0.1.
Чистий Python: без NumPy, сітка будується через range та індекс i.
"""

import math


# --- Вхідні дані варіанта 1 ---
left = 0.0
right = 1.0
h = 0.1

a = 0.75
b = 1.19
c = -2.5


# --- Перевірка сітки ---
if h <= 0:
    raise ValueError("Крок h має бути додатним.")
if right < left:
    raise ValueError("Права межа має бути не меншою за ліву.")

steps_real = (right - left) / h
steps = round(steps_real)

if not math.isclose(steps_real, steps, rel_tol=0.0, abs_tol=1e-12):
    raise ValueError("Довжина відрізка має ділитися на h на ціле число кроків.")


# --- Кусочно задана функція ---
def piecewise_value(x):
    """Повертає номер гілки та значення функції для x у [0, 1]."""
    if not left <= x <= right:
        raise ValueError("Аргумент поза областю [0, 1].")

    if x < 0.5:
        return 1, a * x + b * math.cos(x)

    return 2, b * x ** 2 + c * math.sin(2 * x)


# --- Таблиця ---
print(" i |   x | гілка |            y")
print("---|-----|-------|-------------")

for i in range(steps + 1):
    x = left + i * h
    branch, y = piecewise_value(x)
    print(f"{i:2d} | {x:3.1f} | {branch:5d} | {y:11.7f}")


# --- Структурні перевірки зі слайда ---
assert steps + 1 == 11
assert piecewise_value(0.0)[0] == 1
assert piecewise_value(0.5)[0] == 2
assert piecewise_value(1.0)[0] == 2
