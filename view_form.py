"""Форма просмотра товара."""
import tkinter as tk
from tkinter import ttk, messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, FONT_SIZE_TITLE, font
)
from resources import load_image, get_product_image


class ViewForm:
    """Форма просмотра выбранного товара."""

    def __init__(self, parent, product, on_add_to_order=None):
        self.product = product
        self.on_add_to_order = on_add_to_order
        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product.name}")
        self.window.geometry("700x600")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.build_ui()

    def build_ui(self):
        # Шапка
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header, text="КАРТОЧКА ТОВАРА",
            font=font(FONT_SIZE_TITLE, bold=True),
            bg=COLOR_SECONDARY_BG
        ).pack(pady=15)

        # Основная область
        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Изображение
        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10)
        img_path = f"resources/{self.product.image}" if self.product.image else None
        photo = get_product_image(img_path, size=(200, 200))
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            img_label.image = photo
            img_label.pack()

        # Информация
        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)

        self._add_field(info_frame, "Производство", self.product.manufacturer)
        self._add_field(info_frame, "Наименование", self.product.name)
        self._add_field(info_frame, "Категория", self.product.category)
        self._add_field(info_frame, "Состав", self.product.composition)
        self._add_field(info_frame, "Цена", f"{self.product.price} руб.")
        self._add_field(info_frame, "Размер", self.product.size)

        # Кнопки
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(
            btn_frame, text="Добавить в заказ",
            command=self.add_to_order,
            bg=COLOR_ACCENT, fg="white",
            font=font(FONT_SIZE_NORMAL),
            padx=15, pady=5
        ).pack(side="left", padx=20)

        tk.Button(
            btn_frame, text="Назад",
            command=self.window.destroy,
            bg=COLOR_ACCENT, fg="white",
            font=font(FONT_SIZE_NORMAL),
            padx=15, pady=5
        ).pack(side="right", padx=20)

    def _add_field(self, parent, label, value):
        """Добавляет поле в форму."""
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=3)
        tk.Label(
            row, text=f"{label}:",
            font=font(FONT_SIZE_HEADER, bold=True),
            bg=COLOR_MAIN_BG, width=15, anchor="w"
        ).pack(side="left")
        tk.Label(
            row, text=str(value) if value else "[Не указано]",
            font=font(FONT_SIZE_NORMAL),
            bg=COLOR_MAIN_BG, anchor="w"
        ).pack(side="left")

    def add_to_order(self):
        """Обработчик кнопки «Добавить в заказ»."""
        if not self.on_add_to_order:
            messagebox.showinfo("Информация", "Функция в разработке")
            return
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return
        try:
            self.on_add_to_order(self.product)
            messagebox.showinfo("Успех", "Товар добавлен в заказ")
        except Exception as e:
            messagebox.showerror("Ошибка заказа", f"Не удалось добавить товар:\n{e}")
