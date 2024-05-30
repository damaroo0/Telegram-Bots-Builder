# tg_bot/keyboards.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from data_base.main import user_profile

#
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_keyboard_buttons = [
    KeyboardButton(text="Future option 1 - Add a new place"),
    KeyboardButton(text="Future option 2 - Open another profile"),
    KeyboardButton(text="Future option 3 - /share_profile"),
    KeyboardButton(text="/help"),
]
main_keyboard.add(*main_keyboard_buttons)

"""
share_profile_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
share_profile_keyboard_buttons = [
    KeyboardButton(text="Future option 1 - Share an active profile"),
    KeyboardButton(text="Future option 2 - Share another profile"),
    KeyboardButton(text="/main"),
]
share_profile_keyboard.add(*share_profile_keyboard_buttons)
"""
#
connection_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
connection_keyboard_buttons = [
    KeyboardButton(text="Sign in and create your first profile"),
    KeyboardButton(text="Future option 1 - Connect to another Users profile"),
    KeyboardButton(text="Future option 3 - "),
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
