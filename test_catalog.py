import db_products as db

def test_db():
    try:
        return isinstance(db.get_all_products(), list)
    except Exception as e:
        print(f"FAIL БД: {e}")
        return False

def test_count():
    return len(db.get_all_products()) > 0

def test_prices():
    for p in db.get_all_products():
        if not isinstance(p.price, (int, float)):
            print(f"FAIL id={p.id}: цена не число")
            return False
    return True

def test_qty():
    for p in db.get_all_products():
        if p.quantity < 0:
            print(f"FAIL id={p.id}: отрицательное количество")
            return False
    return True

def test_names():
    for p in db.get_all_products():
        if not p.name:
            print(f"FAIL id={p.id}: пустое название")
            return False
    return True

def run_all():
    tests = [("БД доступна", test_db), ("Товары загружены", test_count),
             ("Цены числа", test_prices), ("Кол-во >= 0", test_qty),
             ("Названия не пустые", test_names)]
    passed = 0
    for name, fn in tests:
        r = fn()
        print(("OK " if r else "FAIL ") + name)
        if r: passed += 1
    print(f"Пройдено: {passed}/{len(tests)}")

if __name__ == "__main__":
    run_all()
