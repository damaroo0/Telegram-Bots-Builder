# tg_bot/handler.py

from aiogram import types, Bot
from data_base.main import check_user_in_user_table
from keyboards import (
    main_keyboard, connection_keyboard, available_profiles_keyboard
)
# from static_info import ()

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import TOKEN

bot = Bot(token=TOKEN)

# global vars

global user_id
global user_name


class CreateProfileStates(StatesGroup):
    waiting_for_codename = State()
    
# Commands

async def start_command(message: types.Message):
    await message.answer(f"{message.from_user.full_name}, welcome to our bot 'TakeYourJourney'!")
    
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    
    if check_user_in_user_table(user_id, user_name) == True:
        await message.answer(f"The following profiles are assigned to your user, choose the one you want to work with now:", reply_markup=available_profiles_keyboard(user_id=user_id))
    else:
        await message.answer(f"We noticed that this is the first time you've used our bot. What would you like to do next?", reply_markup=connection_keyboard)

# Keyboard answers

async def connection_keyboard_create(message: types.Message, state: FSMContext):
    await message.answer(f"""Enter the code name of your profile or assembling places for you, your couple or you and friends. \n For example: 'Where to go this weekend', 'Romantic trips with your sweetheart', 'Pus trip on the rivers of alcohol'""")
    await CreateProfileStates.waiting_for_codename.set()
    
async def process_codename(message: types.Message, state: FSMContext):
    codename = message.text
    await message.answer(f"Create a new profile with a codename: {codename}")
    await state.update_data(codename=codename)
    await state.finish()