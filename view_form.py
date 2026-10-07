"""Форма просмотра товара."""
import tkinter as tk
from tkinter import ttk, messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, FONT_SIZE_TITLE, font
)
from resources import get_product_image
from order_manager import (
    add_order_to_db,
    add_order_item,
    decrease_product_quantity,
    get_product_quantity
)
from error_handler import validate_positive_int


class ViewForm:
    def __init__(self, parent, product, on_add_to_order=None):
        self.product = product
        self.on_add_to_order = on_add_to_order
        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product.name}")
        self.window.geometry("700x700")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="КАРТОЧКА ТОВАРА",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10)
        img_path = f"resources/{self.product.image}" if self.product.image else None
        photo = get_product_image(img_path, size=(200, 200))
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            img_label.image = photo
            img_label.pack()

        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)

        self._add_field(info_frame, "Производство", self.product.manufacturer)
        self._add_field(info_frame, "Наименование", self.product.name)
        self._add_field(info_frame, "Категория", self.product.category)
        self._add_field(info_frame, "Состав", self.product.composition)
        self._add_field(info_frame, "Цена", f"{self.product.price} руб.")

        qty_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(qty_frame, text="Количество:",
                 font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG).pack(side="left", padx=5)
        self.qty_var = tk.StringVar(value="1")
        tk.Entry(qty_frame, textvariable=self.qty_var, width=5,
                 font=font(FONT_SIZE_NORMAL)).pack(side="left", padx=5)

        size_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        size_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(size_frame, text="Размер:",
                 font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG).pack(side="left", padx=5)
        sizes = [str(self.product.size)] if self.product.size else ["—"]
        self.size_var = tk.StringVar(value=sizes[0])
        ttk.Combobox(size_frame, textvariable=self.size_var,
                     values=sizes, state="readonly", width=5,
                     font=font(FONT_SIZE_NORMAL)).pack(side="left", padx=5)

        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)
        tk.Button(btn_frame, text="Добавить в заказ",
                  command=self.add_to_order,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=20)
        tk.Button(btn_frame, text="Назад",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="right", padx=20)

    def _add_field(self, parent, label, value):
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=3)
        tk.Label(row, text=f"{label}:",
                 font=font(FONT_SIZE_HEADER, bold=True),
                 bg=COLOR_MAIN_BG, width=15, anchor="w").pack(side="left")
        tk.Label(row, text=str(value) if value else "[Не указано]",
                 font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG, anchor="w").pack(side="left")

    def add_to_order(self):
        """Обработчик кнопки «Добавить в заказ»."""
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return

        ok, result = validate_positive_int(self.qty_var.get(), "Количество")
        if not ok:
            messagebox.showwarning("Ошибка ввода", result)
            return
        qty = result

        current_qty = get_product_quantity(self.product.id)
        if qty > current_qty:
            messagebox.showwarning("Ошибка",
                                   f"Доступно только {current_qty} шт.")
            return

        try:
            # Создаём заказ с 1 позицией через create_order (см. order_manager)
            from order_manager import create_order
            size = self.size_var.get()
            price = self.product.price
            items = [(self.product.id, size, qty, price)]
            order_id = create_order("Иванов Иван Иванович", items)

            if order_id is None:
                messagebox.showerror("Ошибка",
                                     "Не удалось создать заказ")
                return

            messagebox.showinfo(
                "Успех",
                f"Заказ №{order_id} оформлен! {qty} шт., размер {size}."
            )
            if self.on_add_to_order:
                self.on_add_to_order()
            self.window.destroy()
        except Exception as e:
            messagebox.showerror(
                "Ошибка заказа",
                f"Не удалось добавить товар:\n{e}"
            )
