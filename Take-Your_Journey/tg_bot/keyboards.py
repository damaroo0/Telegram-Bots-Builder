# tg_bot/keyboards.py

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton,
)

#
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_keyboard_buttons = [

]
main_keyboard.add(*main_keyboard_buttons)

#
connection_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, )
connection_keyboard_buttons = [
    KeyboardButton(text='Create a profile and authorise'),
    KeyboardButton(text='Connect to another Users profile'),
    KeyboardButton(text='Connect to another sample'),
]
connection_keyboard.add(*connection_keyboard_buttons)
