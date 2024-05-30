# tg_bot/handler.py

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data_base.main import check_user_in_user_table, add_user, create_user_profiles_table, profile_creating
from main import _
from keyboards import (
    main_keyboard,
    share_profile_keyboard,
    connection_keyboard,
    available_profiles_keyboard,
)
from static_texts import help_command_text

from config import TOKEN

bot = Bot(token=TOKEN)

# global vars

global user_id, user_name

global current_profile


class CreateProfileStates(StatesGroup):
    waiting_for_profile_nametag = State()


# Commands


async def start_command(message: types.Message):
    global user_id, user_name
    await message.answer(_(
        f"{message.from_user.full_name}, welcome to our bot 'TakeYourJourney'!"
    ))

    user_id = message.from_user.id
    user_name = message.from_user.full_name

    if check_user_in_user_table(user_id, user_name) == True:
        await message.answer(_(
            f"The following profiles are assigned to your user, choose the one you want to work with now:",
            reply_markup=available_profiles_keyboard(user_id=user_id),
        ))
    else:
        await message.answer(_(
            f"We noticed that this is the first time you've used our bot. What would you like to do next?",
            reply_markup=connection_keyboard,
        ))


async def open_main_page(message: types.Message):
    await message.answer("Opening main page", reply_markup=main_keyboard)


async def help_command(message: types.Message):
    header = "Here you can see a list of actions you can perform right now:\n"
    await message.answer(header + "—" * 8 + "\n" + "".join(help_command_text))


async def share_profile(message: types.Message):
    await message.answer("Opening a share profile keyboard", reply_markup=share_profile_keyboard)
    
    
async def create_new_profile(message: types.Message, state: FSMContext):
    await message.answer(
        f"Please enter a name to create a new profile:"
    )
    
    await CreateProfileStates.waiting_for_profile_nametag.set()


# Keyboard answers


async def connection_keyboard_create(message: types.Message, state: FSMContext):
    await message.answer(
        f"Adding you to the system.... \n" f"Creating a table of visits..."
    )
    add_user(user_id=user_id, user_name=user_name)
    create_user_profiles_table(user_id=user_id)

    await message.answer(
        f"Enter the profile nametag for your first profile for assembling places for you, your couple, or you and friends. For example:\n"
        f"- 'Where to go this weekend'\n"
        f"- 'Romantic trips with your sweetheart'\n"
        f"- 'Pus trip on the rivers of alcohol'"
    )

    await CreateProfileStates.waiting_for_profile_nametag.set()


# universal function


async def process_profile_nametag(message: types.Message, state: FSMContext):
    global user_id

    profile_nametag = message.text
    await message.answer(f'Create a new profile with a name: "{profile_nametag}"')
    await state.update_data(codename=profile_nametag)
    await state.finish()

    profile_creating(user_id=user_id, profile_nametag=profile_nametag)

    global current_profile
    current_profile = f"{user_id}-{profile_nametag}"

    await message.answer(
        f"Welcome to your new profile '{user_id}-{profile_nametag}', below you can see all the features of our bot:",
        reply_markup=main_keyboard,
    )
