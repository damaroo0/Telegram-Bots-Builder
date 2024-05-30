# tg_bot/main.py

import sys, os

parent_dir = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)
sys.path.append(parent_dir)

import logging


from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command, Text

from config import TOKEN, I18N_DOMAIN, LOCALES_DIR

from data_base.main import check_if_database_exists
from handler import (
    CreateProfileStates,
    start_command,
    open_main_page,
    help_command,
    create_new_profile,
    share_profile,
    connection_keyboard_create,
    process_profile_nametag,
)

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, storage=storage)

# configuring i18n - localisations for the bot
i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
dispatcher.middleware.setup(i18n)
_ = i18n.gettext

# Registering handlers
# commands
dispatcher.register_message_handler(start_command, Command("start"))

dispatcher.register_message_handler(open_main_page, Command("main"))
dispatcher.register_message_handler(help_command, Command("help"))

dispatcher.register_message_handler(share_profile, Command(_("share_profile")))

# buttons rwgistration
dispatcher.register_message_handler(
    connection_keyboard_create,
    Text(_(equals="Sign in and create your first profile")),
)
dispatcher.register_message_handler(
    process_profile_nametag, state=CreateProfileStates.waiting_for_profile_nametag
)

dispatcher.register_message_handler(create_new_profile, Text(_(equals="Create new profile")))

dispatcher.register_message_handler(Text(_(equals="Connect to another Users profile")))


#
async def on_startup(_):
    print("Start bot session. To end session, press the combination 'CTRL' + 'C'")
    check_if_database_exists()


async def on_shutdown(_):
    print("Bot stopped")


#
if __name__ == "__main__":
    executor.start_polling(
        dispatcher=dispatcher, on_startup=on_startup, on_shutdown=on_shutdown
    )
