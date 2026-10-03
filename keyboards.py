from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from products import PRODUCTS


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Каталог визуалов", callback_data="catalog")],
        [InlineKeyboardButton(text="ℹ️ О нас", callback_data="about"),
         InlineKeyboardButton(text="💬 Поддержка", callback_data="support")],
    ])


def catalog_menu() -> InlineKeyboardMarkup:
    rows = []
    for p in PRODUCTS:
        rows.append([InlineKeyboardButton(text=f"{p['name']} — {p['price']}", callback_data=f"buy:{p['id']}")])
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def product_menu(product_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Купить", callback_data=f"order:{product_id}")],
        [InlineKeyboardButton(text="⬅️ К каталогу", callback_data="catalog")],
    ])
