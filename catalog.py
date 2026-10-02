"""Каталог товаров — простая версия."""
import tkinter as tk
from config import COLOR_HIGHLIGHT, FONT_FAMILY


def create_product_card(parent, product):
    """Создаёт карточку товара."""
    qty = product.quantity
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else "white"

    # Карточка
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    # Текстовая часть
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(
        text_frame, text=product.name,
        font=(FONT_FAMILY, 14, "bold"),
        bg=bg_color, anchor="w"
    ).pack(fill="x")

    tk.Label(
        text_frame, text=f"Категория: {product.category}",
        font=(FONT_FAMILY, 11), bg=bg_color, anchor="w"
    ).pack(fill="x")

    tk.Label(
        text_frame, text=f"Количество: {product.indicator()} ({qty})",
        font=(FONT_FAMILY, 11), bg=bg_color, anchor="w"
    ).pack(fill="x")

    tk.Label(
        text_frame, text=f"{product.price} руб.",
        font=(FONT_FAMILY, 14, "bold"),
        bg=bg_color, anchor="e"
    ).pack(fill="x")

    return card