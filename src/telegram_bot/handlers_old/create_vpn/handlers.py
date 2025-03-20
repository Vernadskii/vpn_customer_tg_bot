import os
import traceback

from telegram import CallbackQuery

from telegram_bot.handlers.onboarding.keyboards import make_keyboard_for_start_command
from telegram_bot.handlers.onboarding.static_text import MAIN_MENU
from telegram_bot.main import bot
from telegram_bot.vpn_service.service import get_config
from telegram_bot.vpn_service.utils import create_config_file_async


async def create_vpn_workflow(query: CallbackQuery):
    # Step 1: Send a message to the user
    await query.edit_message_text(text="Preparing your VPN config...")

    file_name = f"vpn_config_{query.id[-5:-1]}.conf"
    file_path = f"{os.getcwd()}/{file_name}"

    try:
        # Step 2: Fetch the config from the vpn_service
        config = await get_config()
        # Step 3: create config file
        await create_config_file_async(file_path, config)
        # Step 4: Send the config to the user
        await bot.send_document(
            chat_id=query.from_user.id, caption='This is your personal VPN config file', document=file_path,
        )

    except Exception as ex:
        await query.edit_message_text(text="Failed to fetch VPN config. Please try again later...")
        print(traceback.format_exc())
        # TODO: add messaging to admins + logging
    else:
        await query.delete_message()
    finally:
        await bot.send_message(chat_id=query.from_user.id, text=MAIN_MENU, reply_markup=make_keyboard_for_start_command())
        if os.path.exists(file_path):
            os.remove(file_path)

