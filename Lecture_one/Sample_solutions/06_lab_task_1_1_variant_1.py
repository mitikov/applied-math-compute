"""Лабораторна 1, завдання 1.1, демонстраційний варіант 1.

Формули з матеріалів:
    a = 2*cos(x - pi/6)*b / (1/2 + sin(y)^2)
    m = 1 + z^2 / (3 + y^2/5)

Використовується лише стандартний модуль math.
"""

import math


# --- Вхідні дані варіанта 1 ---
x = 1.45
y = -1.22
z = 3.5
b = 3.07


# --- Перша величина a ---
numerator_a = 2 * math.cos(x - math.pi / 6) * b
denominator_a = 0.5 + math.sin(y) ** 2

a = numerator_a / denominator_a


# --- Друга величина m ---
denominator_m = 3 + y ** 2 / 5
m = 1 + z ** 2 / denominator_m


# --- Результат ---
print(f"a = {a:.8f}")
print(f"m = {m:.8f}")


# --- Проміжні значення для ручної перевірки ---
print("\nПроміжна перевірка:")
print(f"чисельник a   = {numerator_a:.8f}")
print(f"знаменник a   = {denominator_a:.8f}")
print(f"знаменник m   = {denominator_m:.8f}")
