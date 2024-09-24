from telegram import Update
from telegram.ext import CallbackContext

from telegram_bot.handlers.create_vpn.handlers import create_vpn_workflow
from telegram_bot.handlers.onboarding import static_text
from telegram_bot.handlers.onboarding.static_text import PRICE, CREATE_VPN, MAIN_MENU, ONBOARDING_BUTTONS_QUERY
from django_apps.users.models import User
from telegram_bot.handlers.onboarding.keyboards import make_keyboard_for_start_command
from telegram_bot.handlers.price.keyboards import make_keyboard_for_price_command
from telegram_bot.handlers.price.static_text import PRICE_TEXT


async def command_start(update: Update, context: CallbackContext) -> None:
    u, created = await User.get_user_and_created(update, context)

    if created:
        text = static_text.START_CREATED.format(first_name=u.username)
    else:
        text = static_text.START_OLD_USER.format(first_name=u.username)

    await update.message.reply_text(text=text, reply_markup=make_keyboard_for_start_command())


async def handler_main_menu(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    callback_mapper = {
        ONBOARDING_BUTTONS_QUERY[MAIN_MENU]: query.edit_message_text(
            text=MAIN_MENU, reply_markup=make_keyboard_for_start_command(),
        ),
        ONBOARDING_BUTTONS_QUERY[PRICE]: query.edit_message_text(
            text=PRICE_TEXT, reply_markup=make_keyboard_for_price_command(),
        ),
        ONBOARDING_BUTTONS_QUERY[CREATE_VPN]: create_vpn_workflow(query)
    }
    if action := callback_mapper.get(query.data):
        await action
    else:
        await query.edit_message_text(text=f"You selected {query.data}, but there is no handler for it rn")
