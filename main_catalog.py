import tkinter as tk
import db_products as db


def show_catalog():
    root = tk.Tk()
    root.title("Каталог товаров")
    root.geometry("800x600")

    # Используем Text — на macOS работает надёжнее
    text = tk.Text(
        root,
        font=("Arial", 14),
        bg="white",
        fg="black",
        wrap="word",
        padx=15,
        pady=15
    )
    text.pack(fill="both", expand=True)

    text.insert("end", "=== КАТАЛОГ ТОВАРОВ ===\n\n")

    # Загружаем товары
    products = db.get_all_products()
    print(f"Загружено товаров: {len(products)}")

    for p in products:
        qty = p.quantity

        # Товар с малым количеством — помечаем звёздочкой
        marker = "⚠ " if qty <= 3 else "   "

        text.insert("end", f"{marker}{p.name}\n")
        text.insert("end", f"      Категория:   {p.category}\n")
        text.insert("end", f"      Количество: {p.indicator()} ({qty})\n")
        text.insert("end", f"      Цена:       {p.price} руб.\n\n")

    # Делаем только для чтения
    text.config(state="disabled")

    root.mainloop()


if __name__ == "__main__":
    show_catalog()