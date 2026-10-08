# Практичне заняття 2. Частина 2 — операції над матрицями через обробку зображень

## Завдання 4. Напрямлені різниці та оператор Собеля

**Мета:** дослідити ядра з додатними й від'ємними вагами, дві компоненти градієнта, карту сили країв та вплив попереднього розмиття.

**Орієнтовний час:** 35 хвилин.

У [завданні 3](task-03.md) сусіди усереднювалися. Тут порівнюватимете значення з протилежних боків пікселя. Виконайте **обидві частини: А та Б**.

### Підготовка

1. Створіть окремий notebook у Jupyter або [Google Colab](https://colab.research.google.com/) із `numpy` та `matplotlib`. Виконуйте блоки по порядку; можна працювати в одному `.py` файлі.
2. Використайте ту саму тестову сцену, що й у завданні 3: прямокутник і дві окремі точки.
3. До запуску позначте, де очікуєте сильну відповідь: всередині однорідних областей, на межах чи біля точок. Поясніть прогноз.

### Початковий код

```python
import numpy as np
import matplotlib.pyplot as plt

G = np.full((13, 15), 30, dtype=np.uint8)
G[3:10, 6:12] = 210
G[1, 2] = 255
G[6, 8] = 0

def local_filter(image, kernel, border="edge"):
    image = np.asarray(image, dtype=np.float64)
    kernel = np.asarray(kernel, dtype=np.float64)
    if image.ndim != 2 or kernel.ndim != 2:
        raise ValueError("Потрібні двовимірні матриці")
    kh, kw = kernel.shape
    if kh % 2 == 0 or kw % 2 == 0:
        raise ValueError("Розміри ядра мають бути непарними")
    if border not in ("edge", "constant"):
        raise ValueError("border: edge або constant")
    padded = np.pad(image, ((kh // 2, kh // 2), (kw // 2, kw // 2)),
                    mode=border)
    result = np.empty_like(image)
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            patch = padded[row:row + kh, col:col + kw]
            result[row, col] = np.sum(patch * kernel)
    return result

def show_fields(image, gx, gy, magnitude, limit, label):
    fig, axes = plt.subplots(1, 4, figsize=(15, 4))
    specs = [
        (image, "Зображення", "gray", 0, 255),
        (gx, label + ": Gx", "coolwarm", -limit, limit),
        (gy, label + ": Gy", "coolwarm", -limit, limit),
        (magnitude, label + ": сила", "gray", 0, np.sqrt(2) * limit)
    ]
    for ax, (data, title, cmap, vmin, vmax) in zip(axes, specs):
        plot = ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax,
                         interpolation="nearest", origin="upper")
        ax.set_title(title)
        ax.set_xlabel("Стовпець")
        ax.set_ylabel("Рядок")
        fig.colorbar(plot, ax=ax, shrink=0.65)
    plt.tight_layout()
    plt.show()

def show_gray(items):
    fig, axes = plt.subplots(1, len(items), figsize=(4 * len(items), 4))
    for ax, (data, title) in zip(np.atleast_1d(axes), items):
        ax.imshow(data, cmap="gray", vmin=0, vmax=255,
                  interpolation="nearest", origin="upper")
        ax.set_title(title)
        ax.set_xlabel("Стовпець")
        ax.set_ylabel("Рядок")
    plt.tight_layout()
    plt.show()

controls = [(6, 5), (2, 9), (11, 13)]
show_gray([(G, "Початкова сцена")])
```

Функція множить відповідні елементи околу та ядра й підсумовує добутки. Як і раніше, це кореляція без перевертання ядра. Для антисиметричних ядер різниць перевертання змінило б знак відповіді; у цьому завданні користуємося наведеними ядрами та їхньою домовленістю про знак.

## А. Напрямлені різниці

**Питання досліду:** чому межі різної орієнтації потребують різних операторів?

Використайте два ядра:

- `Kx = [-1, 0, 1]`: правий сусід мінус лівий.
- `Ky = [-1, 0, 1].T`: нижній сусід мінус верхній.

Отже, Gx показує зміну вздовж стовпців, Gy — вздовж рядків. Вісь рядків на зображенні спрямована вниз.

### Дії

1. До запуску обчисліть Gx у координаті `(6,5)` і Gy у `(2,9)` за значеннями G. Спрогнозуйте знак та відповідь обох компонент у `(11,13)`.
2. Запустіть блок. Розгляньте компоненти окремо, потім їхню спільну силу `sqrt(Gx² + Gy²)`.
3. Помножте **обидва** ядра на −1, повторіть запуск і порівняйте компоненти та силу. Потім поверніть початкові ядра.

```python
kx = np.array([[-1, 0, 1]], dtype=np.float64)
ky = kx.T.copy()

gx = local_filter(G, kx)
gy = local_filter(G, ky)
magnitude = np.hypot(gx, gy)

for row, col in controls:
    print((row, col), "Gx =", gx[row, col], "Gy =", gy[row, col],
          "сила =", round(float(magnitude[row, col]), 2))

show_fields(G, gx, gy, magnitude, limit=255, label="Різниці")

gx_reversed = local_filter(G, -kx)
gy_reversed = local_filter(G, -ky)
print("Зміна знаків ядер зберегла силу:",
      np.allclose(magnitude, np.hypot(gx_reversed, gy_reversed)))
```

| Контрольна координата | Прогноз Gx | Фактичне Gx | Прогноз Gy | Фактичне Gy | Сила |
| --- | ---: | ---: | ---: | ---: | ---: |
| (6,5) | | | | | |
| (2,9) | | | | | |
| (11,13) | | | | | |

### Питання до частини А

- Яка компонента сильніше реагує на вертикальні межі прямокутника, а яка — на горизонтальні? Не плутайте напрям зміни з орієнтацією самої межі.
- Що означає додатна й від'ємна відповідь? Чому різні боки прямокутника можуть мати протилежні знаки?
- Чому зміна знаків обох ядер не змінює силу? Чому заміна сили на Gx+Gy могла б втратити частину меж?

## Б. Оператор Собеля

**Питання досліду:** що змінюється, якщо напрямлену різницю поєднати зі зважуванням сусідніх рядків або стовпців?

Собель використовує два ядра 3×3. Одне знаходить зміни вздовж стовпців, друге — вздовж рядків. Коефіцієнти `1,2,1` додають зважування в перпендикулярному напрямку.

### Дії

1. До запуску випишіть окіл 3×3 навколо `(6,5)`. Вручну обчисліть його поелементні добутки з `sobel_x` та їхню суму.
2. Запустіть блок. Порівняйте числові результати зі звичайними різницями у тих самих координатах.
3. Послідовно встановіть пороги `120`, `400`, `700`. Поріг застосовується до сили Собеля **до будь-якого перетворення на uint8**.
4. Заповніть таблицю. Зверніть увагу на межі прямокутника й відповіді біля окремих точок.

```python
sobel_x = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
], dtype=np.float64)
sobel_y = sobel_x.T.copy()

sx = local_filter(G, sobel_x)
sy = local_filter(G, sobel_y)
sobel_magnitude = np.hypot(sx, sy)

threshold = 400  # Дослідіть 120, 400, 700.
edge_mask = np.where(sobel_magnitude > threshold, 255, 0).astype(np.uint8)

print("Окіл (6,5):\n", G[5:8, 4:7])
print("Суми коефіцієнтів:", sobel_x.sum(), sobel_y.sum())
for row, col in controls:
    print((row, col), "Sx =", sx[row, col], "Sy =", sy[row, col],
          "сила =", round(float(sobel_magnitude[row, col]), 2))
print("Максимальна сила:", sobel_magnitude.max())
print("Позначених пікселів:", np.count_nonzero(edge_mask))
print("Форма й тип сили:", sobel_magnitude.shape, sobel_magnitude.dtype)

show_fields(G, sx, sy, sobel_magnitude, limit=4 * 255, label="Собель")
show_gray([(G, "Початкове"),
           (edge_mask, f"Сила Собеля > {threshold}")])
```

| Поріг | Вхід | Прогноз збережених меж | Кількість позначених пікселів | Що сталося біля окремих точок |
| ---: | --- | --- | ---: | --- |
| 120 | Початкова G | | | |
| 400 | Початкова G | | | |
| 700 | Початкова G | | | |
| 400 | Після усереднення 3×3 | | | |

### Попереднє розмиття

1. Перед запуском спрогнозуйте, що буде з відповідями біля окремих точок і з силою меж прямокутника.
2. Виконайте усереднення 3×3, потім Собель. Порівняйте з Собелем на початковій G за **однакового порога 400**.
3. Доповніть останній рядок таблиці. Оцініть не тільки кількість позначок, а й те, які межі збереглися.

```python
blurred = local_filter(G, np.ones((3, 3)) / 9)

bsx = local_filter(blurred, sobel_x)
bsy = local_filter(blurred, sobel_y)
blurred_magnitude = np.hypot(bsx, bsy)

comparison_threshold = 400
mask_original = np.where(sobel_magnitude > comparison_threshold,
                         255, 0).astype(np.uint8)
mask_blurred = np.where(blurred_magnitude > comparison_threshold,
                        255, 0).astype(np.uint8)

print("Позначок до розмиття:", np.count_nonzero(mask_original))
print("Позначок після розмиття:", np.count_nonzero(mask_blurred))
print("Максимальна сила до:", sobel_magnitude.max(),
      "після:", blurred_magnitude.max())

show_gray([
    (G, "Початкове"), (blurred, "Усереднення 3×3"),
    (mask_original, "Собель без розмиття"),
    (mask_blurred, "Собель після розмиття")
])
```

### Питання до частини Б

- Чому сума коефіцієнтів кожного ядра дорівнює нулю? Що це означає для рівномірної ділянки?
- Чому сила Собеля може перевищувати 255? Чому її не можна одразу записати в uint8?
- Що дає і що забирає попереднє розмиття? Чи є менша кількість позначених пікселів достатнім доказом кращого результату?

**Межі моделі:** карта країв показує зміни інтенсивності, а не назви або межі розпізнаних об'єктів. Окрема точка теж створює перепад. Отримані межі можуть бути товщими за один піксель: тут немає стоншення контурів або інших етапів складніших детекторів.

Компоненти й сила зберігаються у float64. Колірні шкали простих різниць і Собеля мають різні межі, позначені біля графіків: порівнюйте числа, а не лише яскравість карт. Пороги двох операторів не можна безпосередньо зіставляти через різний масштаб коефіцієнтів. Для порівняння до й після розмиття використовується той самий оператор і поріг.

### Що здати

Notebook або `.py` файл із результатами; дві таблиці; ручні розрахунки частин А та Б; перевірку зміни знаків ядер; відповіді на питання та висновок у 3–5 реченнях.

Збережіть карти простих різниць; карти Собеля та одну порогову маску; порівняння Собеля до й після розмиття. Інші результати внесіть у таблиці.

Матеріали розмістіть у власному fork у папці `Lecture_two_part2` за [форматом виконання](../Lecture_two/Hometask.md#формат-виконання). Перед здачею виконайте всі комірки з чистого kernel і перевірте файли на GitHub.
