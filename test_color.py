from catalog import _get_card_color
from styles import COLOR_HIGHLIGHT, COLOR_MAIN_BG

def test_color():
    cases = [(10,COLOR_MAIN_BG,"10>3"),(5,COLOR_MAIN_BG,"5>3"),
             (4,COLOR_MAIN_BG,"4>3"),(3,COLOR_HIGHLIGHT,"3<=3 граница"),
             (2,COLOR_HIGHLIGHT,"2<=3"),(0,COLOR_HIGHLIGHT,"0<=3"),
             (100,COLOR_MAIN_BG,"большое"),(-1,COLOR_HIGHLIGHT,"отриц")]
    passed = 0
    for qty, exp, c in cases:
        r = _get_card_color(qty)
        ok = "OK" if r == exp else "FAIL"
        if r == exp: passed += 1
        print(f"{ok} qty={qty}: {r} ({c})")
    print(f"Пройдено: {passed}/{len(cases)}")

if __name__ == "__main__":
    test_color()
