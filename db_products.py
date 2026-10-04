"""Работа с базой данных товаров."""
import sqlite3
from config import DB_PATH
from models import Product


def get_all_products():
    """Возвращает список всех товаров из БД."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, название, категория, производство, состав,
               цена, количество, изображение, размер
        FROM Товар
    """)
    rows = cursor.fetchall()
    conn.close()

    products = []
    for row in rows:
        products.append(Product(
            row[0],  # id
            row[1],  # название
            row[2],  # категория
            row[3],  # производство
            row[4],  # состав
            row[5],  # цена
            row[6],  # количество
            row[7],  # изображение
            row[8],  # размер
        ))
    return products