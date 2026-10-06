"""Тестирование каталога (интеграционные тесты)."""
import db_products as db


def test_db_available():
    try:
        products = db.get_all_products()
        return isinstance(products, list)
    except Exception as e:
        print(f"FAIL БД недоступна: {e}")
        return False


def test_products_count():
    products = db.get_all_products()
    return len(products) > 0


def test_prices_are_numbers():
    products = db.get_all_products()
    for p in products:
        if not isinstance(p.price, (int, float)):
            print(f"FAIL Товар id={p.id}: цена не число")
            return False
    return True


def test_quantity_not_negative():
    products = db.get_all_products()
    for p in products:
        if p.quantity < 0:
            print(f"FAIL Товар id={p.id}: отрицательное количество")
            return False
    return True


def test_names_not_empty():
    """Дописано (задание 6.6)."""
    products = db.get_all_products()
    for p in products:
        if not p.name:
            print(f"FAIL Товар id={p.id}: пустое название")
            return False
    return True


def run_all_tests():
    tests = [
        ("БД доступна", test_db_available),
        ("Товары загружены", test_products_count),
        ("Все цены — числа", test_prices_are_numbers),
        ("Количество не отрицательное", test_quantity_not_negative),
        ("Названия не пустые", test_names_not_empty),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ КАТАЛОГА")
    print("=" * 60)

    passed = 0
    for name, func in tests:
        result = func()
        status = "OK" if result else "FAIL"
        if result:
            passed += 1
        print(f"{status} {name}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(tests)}")


if __name__ == "__main__":
    run_all_tests()
