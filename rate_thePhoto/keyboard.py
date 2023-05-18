# keyboard.py

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
    InlineKeyboardMarkup, InlineKeyboardButton,
)

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_buttons = [
    KeyboardButton(text = "/help", ),
    KeyboardButton(text = "/description", ),
    KeyboardButton(text = "Random Photo", ),
]
main_keyboard.add(*main_buttons)

photo_nav_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
photo_nav_buttons = [
    KeyboardButton("random", ),
    KeyboardButton("Main Page")
]
photo_nav_keyboard.add(*photo_nav_buttons)

inline_photo_keyboard = InlineKeyboardMarkup()
ipk_buttons = [
    InlineKeyboardButton(text="random", callback_data="random"),
    InlineKeyboardButton(text="", callback_data=""),
    InlineKeyboardButton(text="", callback_data=""),
]
inline_photo_keyboard.add(*ipk_buttons)
