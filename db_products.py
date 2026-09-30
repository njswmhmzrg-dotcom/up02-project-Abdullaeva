"""Загрузка товаров из БД с расширенным выводом."""
import sqlite3
from config import DB_PATH

def get_all_products():
    """Возвращает список всех товаров."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    products = cur.fetchall()
    conn.close()
    return products

def get_products_by_category(category):
    """Товары по категории."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE категория = ?", (category,))
    products = cur.fetchall()
    conn.close()
    return products

def get_products_low_stock():
    """Товары с количеством <= 3."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= 3")
    products = cur.fetchall()
    conn.close()
    return products

def get_categories():
    """Список всех категорий."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT категория FROM Товар ORDER BY категория")
    categories = [row[0] for row in cur.fetchall()]
    conn.close()
    return categories

def print_catalog(products):
    """Каталог с индикатором."""
    print(f"\n{'=' * 60}")
    print(f"КАТАЛОГ ({len(products)} товаров)")
    print("=" * 60)
    
    for p in products:
        name = p[1]
        price = p[5]    # Цена
        qty = p[6]      # Количество
        
        # Логика индикатора
        if qty > 5:
            indicator = "МНОГО"
        else:
            indicator = "МАЛО"
            
        # Значок для товаров с низким остатком
        warning = "⚠️" if qty <= 3 else ""
        
        print(f"{name} — {price} руб. ({qty} шт.) -> {indicator} {warning}")

if __name__ == "__main__":
    # 1. Выводим весь каталог
    all_products = get_all_products()
    print_catalog(all_products)
    
    # 2. Выводим список категорий
    cats = get_categories()
    print(f"\nДоступные категории: {', '.join(cats)}")
    
    # 3. Выводим товары с низким остатком
    low_stock = get_products_low_stock()
    print("\nТовары с низким остатком (<=3):")
    for p in low_stock:
        print(f"- {p[1]} ({p[6]} шт.)")