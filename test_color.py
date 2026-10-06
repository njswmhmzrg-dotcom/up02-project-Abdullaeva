"""Тестирование подсветки #ff8080."""
from catalog import _get_card_color
from styles import COLOR_HIGHLIGHT, COLOR_MAIN_BG


def test_color():
    test_cases = [
        (10, COLOR_MAIN_BG, "10 > 3"),
        (5, COLOR_MAIN_BG, "5 > 3"),
        (4, COLOR_MAIN_BG, "4 > 3"),
        (3, COLOR_HIGHLIGHT, "3 <= 3 (граница!)"),
        (2, COLOR_HIGHLIGHT, "2 <= 3"),
        (0, COLOR_HIGHLIGHT, "0 <= 3"),
        # Дописано (задание 5.6)
        (100, COLOR_MAIN_BG, "большое число"),
        (-1, COLOR_HIGHLIGHT, "отрицательное"),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ПОДСВЕТКИ")
    print("=" * 60)

    passed = 0
    for qty, expected, comment in test_cases:
        result = _get_card_color(qty)
        status = "OK" if result == expected else "FAIL"
        if result == expected:
            passed += 1
        print(f"{status} qty={qty}: {result} (ожидалось {expected}) — {comment}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    test_color()
