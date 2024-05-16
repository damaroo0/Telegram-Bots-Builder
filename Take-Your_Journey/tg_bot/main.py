# tg_bot/main.py

import logging
import os, sys


from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command, Text

parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.append(parent_dir)

from data_base.main import check_if_database_existas

from config import TOKEN
from handler import (
    start_command, connection_keyboard_create
)

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, storage)

# Registering handlers
dispatcher.register_message_handler(start_command, Command("start"))

dispatcher.register_message_handler(connection_keyboard_create, Text(equel='Create a profile and authorise'))

#
async def on_startup(_):
    print("Start bot session. To end session, press the combination 'CTRL' + 'C'")
    check_if_database_existas()

async def on_shutdown(_):
    print("Bot stopped")

#
if __name__ == "__main__":
    executor.start_polling(dispatcher=dispatcher, on_startup=on_startup, on_shutdown=on_shutdown)
