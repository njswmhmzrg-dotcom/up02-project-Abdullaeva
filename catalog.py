"""Каталог товаров по макету."""
import tkinter as tk
from PIL import Image, ImageTk
import os
from config import COLOR_HIGHLIGHT, FONT_FAMILY


def create_product_card(parent, product):
    """Создаёт карточку товара по макету."""
    qty = product.quantity
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else "white"

    # Карточка – рамка со всех сторон
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    # === Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    # Путь к картинке товара
    img_name = product.image if product.image else "picture.png"
    image_path = os.path.join("resources", img_name)

    # Если картинки нет — берём заглушку
    if not os.path.exists(image_path):
        image_path = os.path.join("resources", "picture.png")

    try:
        img = Image.open(image_path).resize((120, 120))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo  # Сохраняем ссылку, иначе картинка исчезнет!
        img_label.pack()
    except Exception:
        tk.Label(
            img_frame, text="[НЕТ ФОТО]", bg=bg_color,
            width=15, height=5
        ).pack()

    # === Текстовая часть (справа) ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Производство | Наименование
    title = f"{product.manufacturer} | {product.name}"
    tk.Label(
        text_frame, text=title,
        font=(FONT_FAMILY, 14, "bold"),
        bg=bg_color, anchor="w"
    ).pack(fill="x")

    # Категория
    tk.Label(
        text_frame, text=f"Категория: {product.category}",
        font=(FONT_FAMILY, 11), bg=bg_color, anchor="w"
    ).pack(fill="x")

    # Количество
    indicator = product.indicator()
    tk.Label(
        text_frame, text=f"Количество: {indicator} ({qty})",
        font=(FONT_FAMILY, 11), bg=bg_color, anchor="w"
    ).pack(fill="x")

    # Состав
    tk.Label(
        text_frame, text=f"Состав: {product.composition}",
        font=(FONT_FAMILY, 11), bg=bg_color, anchor="w"
    ).pack(fill="x")

    # Размер (если есть)
    if product.size:
        tk.Label(
            text_frame, text=f"Размер: {product.size}",
            font=(FONT_FAMILY, 11), bg=bg_color, anchor="w"
        ).pack(fill="x")

    # Цена (справа)
    tk.Label(
        text_frame, text=f"{product.price} руб.",
        font=(FONT_FAMILY, 14, "bold"),
        bg=bg_color, anchor="e"
    ).pack(fill="x")

    return card