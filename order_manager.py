"""Работа с заказами."""
import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    """Соединение с БД."""
    return sqlite3.connect(DB_PATH)


def add_order_to_db(client, date=None):
    """Добавляет новый заказ в БД (без позиций)."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Заказ (дата, клиент) VALUES (?, ?)",
        (date, client)
    )
    conn.commit()
    order_id = cur.lastrowid
    conn.close()
    return order_id


def add_order_item(order_id, product_id, size, quantity, price):
    """Добавляет позицию в состав заказа."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Состав_заказа "
        "(заказ_id, товар_id, размер, количество, цена) "
        "VALUES (?, ?, ?, ?, ?)",
        (order_id, product_id, size, quantity, price)
    )
    conn.commit()
    item_id = cur.lastrowid
    conn.close()
    return item_id


def create_order(client, items):
    """
    Создаёт заказ с несколькими позициями.
    :param client: ФИО клиента
    :param items: список кортежей (product_id, size, quantity, price)
    :return: id заказа или None
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            "INSERT INTO Заказ (дата, клиент) VALUES (?, ?)",
            (date, client)
        )
        order_id = cur.lastrowid

        for product_id, size, quantity, price in items:
            cur.execute(
                "INSERT INTO Состав_заказа "
                "(заказ_id, товар_id, размер, количество, цена) "
                "VALUES (?, ?, ?, ?, ?)",
                (order_id, product_id, size, quantity, price)
            )

        conn.commit()
        return order_id
    except Exception as e:
        conn.rollback()
        print(f"Ошибка создания заказа: {e}")
        return None
    finally:
        conn.close()


def update_product_quantity(product_id, new_quantity):
    """Обновляет количество товара в БД."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Товар SET количество = ? WHERE id = ?",
        (new_quantity, product_id)
    )
    conn.commit()
    conn.close()


def get_product_quantity(product_id):
    """Возвращает количество товара по id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0
