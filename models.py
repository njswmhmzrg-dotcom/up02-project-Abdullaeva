"""Модели данных для проекта УП.02."""
from datetime import datetime
from discount import calculate_price_with_discount

class Product:
    def __init__(self, product_id, name, category, price, quantity):
        self.id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    def total(self):
        return self.price * self.quantity

    def price_with_discount_auto(self, date=None):
        if date is None:
            date = datetime.now()
        return calculate_price_with_discount(self.id, self.price, date)

    def indicator(self):
        return "много" if self.quantity > 5 else "мало"

    def info(self):
        return (f"{self.name} ({self.category}): "
                f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
                f"({self.indicator()})")
                
    def discounted_price(self):
                """Цена со скидкой 25% (упрощённо)."""
                return self.price * 0.75
