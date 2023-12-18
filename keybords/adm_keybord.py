from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from Config import books

def create_keybord():
    builder = InlineKeyboardBuilder()
    for book in books.items():
        builder.row(types.InlineKeyboardButton(text=book[1], callback_data=book[0]))
    return builder.as_markup()