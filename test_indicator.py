from catalog import _indicator

cases = [(10,"много","10>5"),(6,"много","6>5"),(5,"мало","5<=5"),
         (4,"мало","4<=5"),(0,"мало","0<=5"),(100,"много","100>5"),
         (1000,"много","1000>5"),(-1,"мало","отриц")]

passed = 0
for qty, expected, c in cases:
    r = _indicator(qty)
    ok = "OK" if r == expected else "FAIL"
    if r == expected: passed += 1
    print(f"{ok} qty={qty}: {r} ({c})")
print(f"\nПройдено: {passed}/{len(cases)}")
