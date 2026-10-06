"""Модуль работы с ресурсами."""
import os
from PIL import Image, ImageTk

PATH_PICTURE = "resources/picture.png"
PATH_LOGO = "resources/logo.png"
PATH_ICON = "resources/icon.ico"

_image_cache = {}


def load_image(path, size=(100, 100)):
    try:
        if not os.path.exists(path):
            return None
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки {path}: {e}")
        return None


def load_image_proportional(path, max_size=(100, 100)):
    try:
        if not os.path.exists(path):
            return None
        img = Image.open(path)
        img.thumbnail(max_size)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки {path}: {e}")
        return None


def get_product_image(image_path, size=(100, 100)):
    if not image_path or not os.path.exists(image_path):
        return load_image(PATH_PICTURE, size)
    return load_image(image_path, size)


def get_cached_image(path, size):
    key = (path, size)
    if key not in _image_cache:
        _image_cache[key] = load_image(path, size)
    return _image_cache[key]
