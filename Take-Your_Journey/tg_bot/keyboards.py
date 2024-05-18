# tg_bot/keyboards.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from data_base.main import user_profile

#
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_keyboard_buttons = [
    KeyboardButton(text="OPTION 1"),
    KeyboardButton(text="OPTION 2"),
    KeyboardButton(text="OPTION 3"),
    KeyboardButton(text="OPTION 4"),
]
main_keyboard.add(*main_keyboard_buttons)

#
connection_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
connection_keyboard_buttons = [
    KeyboardButton(text="Sign in and create your first profile"),
    KeyboardButton(text="Connect to another Users profile"),
    KeyboardButton(text="Connect to another sample"),
]
connection_keyboard.add(*connection_keyboard_buttons)


#
def available_profiles_keyboard(user_id):
    profiles_names = user_profile(user_id=user_id)
    available_profiles_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for profile_name in profiles_names:
        available_profiles_keyboard.add(KeyboardButton(text=profile_name))
    available_profiles_keyboard.add(KeyboardButton(text="Create new profile"))
    return available_profiles_keyboard
