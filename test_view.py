import tkinter as tk
root = tk.Tk()
root.withdraw()
from view_form import ViewForm

class FakeProduct:
    name = "Кроссовки"
    manufacturer = "Nike"
    category = "Спорт"
    composition = "Кожа"
    price = 7000
    quantity = 8
    image = "sneakers.png"
    size = 42

form = ViewForm(root, FakeProduct())
print("OK: форма создана")
root.mainloop()
