"""Работа с заказами."""
import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def add_order_to_db(client, date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Заказ (дата, клиент) VALUES (?, ?)", (date, client))
    conn.commit()
    order_id = cur.lastrowid
    conn.close()
    return order_id


def add_order_item(order_id, product_id, size, quantity, price):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Состав_заказа (заказ_id, товар_id, размер, количество, цена) "
        "VALUES (?, ?, ?, ?, ?)",
        (order_id, product_id, size, quantity, price)
    )
    conn.commit()
    item_id = cur.lastrowid
    conn.close()
    return item_id


def get_product_quantity(product_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


def update_product_quantity(product_id, new_quantity):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Товар SET количество = ? WHERE id = ?",
                (new_quantity, product_id))
    conn.commit()
    conn.close()


def decrease_product_quantity(product_id, quantity):
    """Уменьшает количество товара на складе."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
        row = cur.fetchone()
        if not row:
            return False
        current = row[0]
        if current < quantity:
            return False
        cur.execute("UPDATE Товар SET количество = количество - ? WHERE id = ?",
                    (quantity, product_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка обновления: {e}")
        return False
    finally:
        conn.close()


def create_order(client, items):
    """Создаёт заказ с несколькими позициями и уменьшает остатки."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute("INSERT INTO Заказ (дата, клиент) VALUES (?, ?)", (date, client))
        order_id = cur.lastrowid

        for product_id, size, quantity, price in items:
            # Проверяем наличие
            cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
            row = cur.fetchone()
            if not row or row[0] < quantity:
                raise ValueError(f"Недостаточно товара id={product_id}")
            # Добавляем позицию
            cur.execute(
                "INSERT INTO Состав_заказа (заказ_id, товар_id, размер, количество, цена) "
                "VALUES (?, ?, ?, ?, ?)",
                (order_id, product_id, size, quantity, price)
            )
            # Уменьшаем остаток
            cur.execute(
                "UPDATE Товар SET количество = количество - ? WHERE id = ?",
                (quantity, product_id)
            )

        conn.commit()
        return order_id
    except Exception as e:
        conn.rollback()
        print(f"Ошибка создания заказа: {e}")
        return None
    finally:
        conn.close()


def get_all_orders():
    """Возвращает список всех заказов."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент FROM Заказ ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_order_items(order_id):
    """Возвращает состав заказа с полной информацией."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT Состав_заказа.id, Товар.название, Товар.производство,
               Состав_заказа.размер, Состав_заказа.количество,
               Состав_заказа.цена
        FROM Состав_заказа
        JOIN Товар ON Состав_заказа.товар_id = Товар.id
        WHERE Состав_заказа.заказ_id = ?
        ORDER BY Состав_заказа.id
    """, (order_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def update_order_date(order_id, new_date):
    """Обновляет дату заказа."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE Заказ SET дата = ? WHERE id = ?",
                    (new_date, order_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка обновления даты: {e}")
        return False
    finally:
        conn.close()


def get_order_by_id(order_id):
    """Возвращает заказ по id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент FROM Заказ WHERE id = ?",
                (order_id,))
    row = cur.fetchone()
    conn.close()
    return row


def delete_order_item(item_id):
    """Удаляет позицию из заказа и восстанавливает остатки."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT товар_id, количество FROM Состав_заказа WHERE id = ?",
                    (item_id,))
        row = cur.fetchone()
        if not row:
            return False
        product_id, quantity = row
        cur.execute("DELETE FROM Состав_заказа WHERE id = ?", (item_id,))
        cur.execute("UPDATE Товар SET количество = количество + ? WHERE id = ?",
                    (quantity, product_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка удаления позиции: {e}")
        return False
    finally:
        conn.close()
