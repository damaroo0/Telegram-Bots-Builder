# handler.py

import random

from aiogram import types, Bot

from static_info import (
    help_list, description_text,
    dev_photo,
)
from keyboard import main_keyboard, photo_nav_keyboard, inline_photo_keyboard
from config import TOKEN

bot = Bot(token=TOKEN)

async def start_command(message: types.Message):
    keyboard = main_keyboard
    await message.answer("Добро пожаловать в главное меню бота!", reply_markup=keyboard)

    await message.delete()

async def help_command(message: types.Message):
    await message.answer(text=help_list, parse_mode='HTML')

    await message.delete()

async def description_command(message: types.Message):
    await message.answer(text=description_text, parse_mode='HTML')
    # await bot.send_sticker(chat_id=message.chat.id, sticker="")

    await message.delete()

async def photo_keyboard(message: types.Message):
    keyboard = photo_nav_keyboard
    await message.answer(text="Что бы получить случайную фотографию, нажмите кнопку 'random'", reply_markup=keyboard)

    await message.delete()

async def randome_photo(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id, photo=random.choice(dev_photo))

async def no_entry(message: types.Message):
    await message.answer("Ведуться работы, не лезь!")
    await bot.send_sticker(chat_id=message.chat.id, sticker="CAACAgIAAxkBAAEJBsFkZlzU0aHU4-8_4afcRdok8VhBlQACMgMAApUlJQstsqnnS5bAVS8E")

    await message.delete()
