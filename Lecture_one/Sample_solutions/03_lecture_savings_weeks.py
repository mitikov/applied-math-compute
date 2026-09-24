"""Лекція 1. Завдання: лічильник тижнів до покупки.

Алгоритм повторює щотижневий внесок, доки поточна сума
не стане не меншою за ціль.
"""


# --- Вхідні дані ---
start_amount = 600.0
target_amount = 1500.0
weekly_contribution = 200.0


# --- Перевірка даних ---
if start_amount < 0 or target_amount < 0:
    raise ValueError("Суми не можуть бути від'ємними.")


# --- Обчислення ---
current_amount = start_amount
weeks = 0

if current_amount < target_amount:
    if weekly_contribution <= 0:
        raise ValueError(
            "Якщо ціль ще не досягнута, щотижневий внесок має бути додатним."
        )

    while current_amount < target_amount:
        current_amount += weekly_contribution
        weeks += 1


# --- Результат ---
print(f"Потрібно повних тижнів: {weeks}")
print(f"Сума після завершення: {current_amount:.2f} грн")

# Для даних 600 -> 1500 при +200 грн/тиждень очікуємо 5 тижнів.
assert weeks == 5
