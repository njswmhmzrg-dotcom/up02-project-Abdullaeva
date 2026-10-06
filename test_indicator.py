from catalog import _indicator

def test_indicator():
    cases = [(10,"много","10>5"),(6,"много","6>5"),(5,"мало","5<=5"),
             (4,"мало","4<=5"),(0,"мало","0<=5"),(100,"много","большое"),
             (1,"мало","минимум"),(-1,"мало","отрицательное")]
    passed = 0
    for qty, exp, c in cases:
        r = _indicator(qty)
        ok = "OK" if r == exp else "FAIL"
        if r == exp: passed += 1
        print(f"{ok} qty={qty}: {r} ({c})")
    print(f"Пройдено: {passed}/{len(cases)}")

if __name__ == "__main__":
    test_indicator()
