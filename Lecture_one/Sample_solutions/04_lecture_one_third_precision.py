"""Лекція 1. Завдання: експеримент з наближенням числа 1/3.

Порівнюємо округлення до 1, 2, 3 і 4 знаків після крапки
та шукаємо мінімальну кількість знаків для похибки <= 0.001.
"""


exact_value = 1 / 3
digits_to_check = [1, 2, 3, 4]
tolerance = 0.001

print("знаки | наближення | абсолютна похибка | достатньо?")
print("------|------------|-------------------|----------")

minimum_digits = None

for digits in digits_to_check:
    approximation = round(exact_value, digits)
    absolute_error = abs(exact_value - approximation)
    is_enough = absolute_error <= tolerance

    print(
        f"{digits:5d} | "
        f"{approximation:10.{digits}f} | "
        f"{absolute_error:17.10f} | "
        f"{'так' if is_enough else 'ні'}"
    )

    if is_enough and minimum_digits is None:
        minimum_digits = digits

print()
if minimum_digits is None:
    print(f"Серед перевірених варіантів немає похибки <= {tolerance}.")
else:
    print(
        f"Мінімум знаків після крапки для похибки <= {tolerance}: "
        f"{minimum_digits}"
    )
