from datetime import datetime
from discount import calculate_price_with_discount


class Product:
    def __init__(self, product_id, name, category, manufacturer,
                 composition, price, quantity, image="", size=""):
        self.id = product_id
        self.name = name
        self.category = category
        self.manufacturer = manufacturer
        self.composition = composition
        self.price = price
        self.quantity = quantity
        self.image = image
        self.size = size

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
        """Цена со скидкой 25%."""
        return self.price * 0.75

    def is_available(self):
        """Товар доступен для заказа?"""
        return self.quantity > 0