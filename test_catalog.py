"""Проверка вывода полей."""
import db_products as db


def test_fields():
    """Проверяет, что все поля на месте."""
    products = db.get_all_products()
    print(f"Всего товаров: {len(products)}")
    errors = 0

    for p in products:
        if not p.name:
            print(f"❌ Товар id={p.id}: нет названия")
            errors += 1
        if p.price is None:
            print(f"❌ Товар id={p.id}: нет цены")
            errors += 1
        if p.quantity is None or p.quantity < 0:
            print(f"❌ Товар id={p.id}: некорректное количество")
            errors += 1

    if errors == 0:
        print("✅ Все товары содержат нужные поля")
    else:
        print(f"❌ Найдено ошибок: {errors}")


def test_images():
    """Проверяет, что хотя бы у одного товара есть изображение."""
    products = db.get_all_products()
    has_image = any(p.image for p in products)
    if has_image:
        print("✅ Есть товары с изображениями")
    else:
        print("❌ Ни у одного товара нет изображения")


if __name__ == "__main__":
    test_fields()
    test_images()