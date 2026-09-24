"""Лекція 1. Завдання: калькулятор фарби.

Чистий Python: використовується лише стандартний модуль math.
Змініть значення у блоці "Вхідні дані" і запустіть файл знову.
"""

import math


# --- Вхідні дані ---
area_m2 = 42.0
coats = 2
rate_l_per_m2_per_coat = 0.12
can_volume_l = 3.0


# --- Перевірка даних ---
if area_m2 < 0:
    raise ValueError("Площа не може бути від'ємною.")
if not isinstance(coats, int) or coats < 0:
    raise ValueError("Кількість шарів має бути цілим невід'ємним числом.")
if rate_l_per_m2_per_coat < 0:
    raise ValueError("Витрата фарби не може бути від'ємною.")
if can_volume_l <= 0:
    raise ValueError("Об'єм банки має бути додатним.")


# --- Обчислення ---
required_l = area_m2 * coats * rate_l_per_m2_per_coat
cans = math.ceil(required_l / can_volume_l) if required_l > 0 else 0
purchased_l = cans * can_volume_l
leftover_l = purchased_l - required_l


# --- Результат ---
print(f"Потрібний об'єм фарби: {required_l:.2f} л")
print(f"Потрібно банок: {cans} по {can_volume_l:g} л")
print(f"Буде куплено: {purchased_l:.2f} л")
print(f"Залишок через фасування: {leftover_l:.2f} л")

# Контрольний випадок зі слайда: рівно 9 л при банці 3 л -> 3 банки.
assert math.ceil(9 / 3) == 3
