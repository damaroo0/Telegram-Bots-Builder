# main.py

import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command, Text

from config import TOKEN
from handler import (
    start_command, help_command, description_command,
    photo_keyboard, randome_photo,
    no_entry,
)

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage)

# Регистрация обработчиков
dp.register_message_handler(start_command, Command("start"))
dp.register_message_handler(help_command, Command("help"))
dp.register_message_handler(description_command, Command("description"))

dp.register_message_handler(photo_keyboard, Text(equals="Random Photo"))
dp.register_message_handler(randome_photo, Text(equals="random"))
dp.register_message_handler(start_command, Text(equals="Main Page"))

async def on_sturtup(_):
    print("Запущен")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_sturtup)
