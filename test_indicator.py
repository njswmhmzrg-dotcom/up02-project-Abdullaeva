"""Тестирование индикатора «много/мало»."""
from catalog import _indicator


def test_indicator():
    test_cases = [
        # Базовые
        (10, "много", "10 > 5"),
        (6, "много", "6 > 5 (граница)"),
        (5, "мало", "5 <= 5 (граница)"),
        (4, "мало", "4 <= 5"),
        (1, "мало", "1 <= 5"),
        (0, "мало", "0 <= 5"),
        (100, "много", "большое число"),
        # ДЗ: 5 дополнительных
        (1000, "много", "очень большое число"),
        (50, "много", "среднее значение"),
        (7, "много", "чуть выше порога"),
        (2, "мало", "чуть ниже порога"),
        (-1, "мало", "отрицательное (крайний случай)"),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ИНДИКАТОРА")
    print("=" * 60)

    passed = 0
    for qty, expected, comment in test_cases:
        result = _indicator(qty)
        status = "OK" if result == expected else "FAIL"
        if result == expected:
            passed += 1
        print(f"{status} qty={qty}: {result} (ожидалось {expected}) — {comment}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    test_indicator()
