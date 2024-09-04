import datetime

from django.utils import timezone
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

from telegram_bot.handlers.onboarding import static_text
from telegram_bot.handlers.onboarding.static_text import REFERRAL, HELP, PRICE, DEPOSIT, MY_BALANCE, MY_VPN, CREATE_VPN, \
    PRICE_TEXT
from telegram_bot.handlers.utils.info import extract_user_data_from_update
from users.models import User
from telegram_bot.handlers.onboarding.keyboards import make_keyboard_for_start_command, make_keyboard_for_price_command


async def command_start(update: Update, context: CallbackContext) -> None:
    u, created = await User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    await update.message.reply_text(text=text, reply_markup=make_keyboard_for_start_command())


async def first_menu_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    # Process the callback data and update the message
    if query.data == CREATE_VPN:
        await query.edit_message_text(text="You selected Option 1")
    elif query.data == MY_VPN:
        await query.edit_message_text(text="You selected Option 2")
    elif query.data == MY_BALANCE:
        await query.edit_message_text(text="You selected Option 3")
    elif query.data == DEPOSIT:
        await query.edit_message_text(text="You selected Option 4")
    elif query.data == PRICE:
        await query.edit_message_text(
            text=PRICE_TEXT, reply_markup=make_keyboard_for_price_command(), parse_mode=ParseMode.MARKDOWN
        )
    elif query.data == HELP:
        await query.edit_message_text(text="You selected Option 6")
    elif query.data == REFERRAL:
        await query.edit_message_text(text="You selected Option 7")