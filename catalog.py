"""Каталог товаров."""
import tkinter as tk
from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from resources import get_product_image


def create_product_card(parent, product, refresh=None):
    """Создаёт карточку товара. refresh — callback для обновления каталога."""
    qty = product.quantity
    bg_color = _get_card_color(qty)

    card = tk.Frame(parent, bg=bg_color, bd=2, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty)

    # Привязка клика ко всем вложенным элементам
    def _bind_all(widget):
        widget.bind("<Button-1>",
                    lambda e: _open_view(parent, product, refresh))
        for child in widget.winfo_children():
            _bind_all(child)
    _bind_all(card)

    return card


def _open_view(parent, product, refresh=None):
    """Открывает форму просмотра товара."""
    from view_form import ViewForm
    ViewForm(parent, product, on_add_to_order=refresh)


def _get_card_color(qty):
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


def _add_image(card, product, bg_color):
    img_frame = tk.Frame(card, bg=bg_color, width=140, height=140)
    img_frame.pack(side="left", padx=10, pady=10)
    img_frame.pack_propagate(False)

    img_path = f"resources/{product.image}" if product.image else None
    photo = get_product_image(img_path, size=(120, 120))

    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo
        img_label.pack(expand=True)
    else:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color, fg="black",
                 font=font(FONT_SIZE_NORMAL)).pack(expand=True)


def _add_text_info(card, product, bg_color, qty):
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    name = product.name if product.name else "[Без названия]"
    production = product.manufacturer if product.manufacturer else "[Без производства]"
    category = product.category if product.category else "[Без категории]"
    composition = product.composition if product.composition else "[Не указан]"
    price = product.price if product.price is not None else 0

    if len(name) > 100:
        name = name[:97] + "..."

    price_str = f"{price:,.0f}".replace(",", " ")
    if price > 1_000_000:
        price_str += " (дорого)"

    _add_label(text_frame, f"{production} | {name}",
               bg_color, bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, f"Категория: {category}", bg_color)
    _add_label(text_frame, f"Количество: {_indicator(qty)} ({qty})", bg_color)
    _add_label(text_frame, f"Состав: {composition}", bg_color)

    if product.size:
        _add_label(text_frame, f"Размер: {product.size}", bg_color)

    _add_label(text_frame, f"{price_str} руб.",
               bg_color, bold=True, size=FONT_SIZE_HEADER, align="e")


def _add_label(parent, text, bg_color, bold=False,
               size=FONT_SIZE_NORMAL, align="w"):
    tk.Label(parent, text=text, font=font(size, bold=bold),
             bg=bg_color, fg="black", anchor=align).pack(fill="x")


def _indicator(qty):
    return "много" if qty > 5 else "мало"
