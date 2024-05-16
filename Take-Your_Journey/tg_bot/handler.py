# tg_bot/handler.py

import sys, os

from aiogram import types, Bot

parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.append(parent_dir)

from data_base.main import check_user_in_database

from keyboards import (
    main_keyboard, connection_keyboard
)
# from static_info import ()

from config import TOKEN

bot = Bot(token=TOKEN)

def __init__(self) -> None:
    self.user_id = None
    self.user_name = None
    
# Commands

async def start_command(message: types.Message):
    await message.answer(f"{message.from_user.full_name}, welcome to our bot 'TakeYourJourney'!")
    
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    
    if check_user_in_database(user_id, user_name) == True:
        await message.answer(f"The table for your id already exists in the data base, what do we do next?", reply_markup=main_keyboard)
    else:
        await message.answer(f"We don't yet have a table with your data and places of interest, what do we do next?", reply_markup=connection_keyboard)

# Keyboard answers

async def connection_keyboard_create(message: types.Message):
    await message.answer(f"Enter the code name of your profile \ assembling places for you, your couple or you and friends. 
                         \n For example: 'Where to go this weekend', 'Romantic trips with your sweetheart', 'Pus trip on the rivers of alcohol'")
    