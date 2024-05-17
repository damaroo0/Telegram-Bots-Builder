# tg_bot/main.py

import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.append(parent_dir)

import logging


from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command, Text

from config import TOKEN

from data_base.main import check_if_database_exists
from handler import (
    CreateProfileStates,
    start_command, 
    connection_keyboard_create, process_codename
)

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, storage=storage)

# Registering handlers
dispatcher.register_message_handler(start_command, Command("start"))

dispatcher.register_message_handler(connection_keyboard_create, Text(equals='Sign in and create your first profile'))
dispatcher.register_message_handler(process_codename, state=CreateProfileStates.waiting_for_codename)

#
async def on_startup(_):
    print("Start bot session. To end session, press the combination 'CTRL' + 'C'")
    check_if_database_exists()

async def on_shutdown(_):
    print("Bot stopped")

#
if __name__ == "__main__":
    executor.start_polling(dispatcher=dispatcher, on_startup=on_startup, on_shutdown=on_shutdown)
