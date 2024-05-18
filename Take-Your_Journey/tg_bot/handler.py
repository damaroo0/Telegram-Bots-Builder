# tg_bot/handler.py

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data_base.main import (
    check_user_in_user_table, add_user
)
from keyboards import main_keyboard, connection_keyboard, available_profiles_keyboard
# from static_info import ()

from config import TOKEN

bot = Bot(token=TOKEN)

# global vars

global user_id
global user_name


class CreateProfileStates(StatesGroup):
    waiting_for_profile_nametag = State()


# Commands


async def start_command(message: types.Message):
    global user_id, user_name
    await message.answer(
        f"{message.from_user.full_name}, welcome to our bot 'TakeYourJourney'!"
    )

    user_id = message.from_user.id
    user_name = message.from_user.full_name

    if check_user_in_user_table(user_id, user_name) == True:
        await message.answer(
            f"The following profiles are assigned to your user, choose the one you want to work with now:",
            reply_markup=available_profiles_keyboard(user_id=user_id),
        )
    else:
        await message.answer(
            f"We noticed that this is the first time you've used our bot. What would you like to do next?",
            reply_markup=connection_keyboard,
        )


# Keyboard answers


async def connection_keyboard_create(message: types.Message, state: FSMContext):
    await message.answer(f"Adding you to the system....")
    # add_user(user_id=user_id, user_name=user_name)

    await message.answer(
        f"Enter the profile nametag for your first profile for assembling places for you, your couple, or you and friends. For example:\n"
        f"- 'Where to go this weekend'\n"
        f"- 'Romantic trips with your sweetheart'\n"
        f"- 'Pus trip on the rivers of alcohol'"
    )
    
    await CreateProfileStates.waiting_for_profile_nametag.set()


async def process_profile_nametag(message: types.Message, state: FSMContext):
    profile_nametag = message.text
    await message.answer(f'Create a new profile with a name: (ничего не создаеться)"{profile_nametag}"')
    await state.update_data(codename=profile_nametag)
    await state.finish()
