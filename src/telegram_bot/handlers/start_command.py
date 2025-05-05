# Вынесена в отдельный файл, чтобы избежать проблем с цикличным импортом.
# start_command используется в start.py, info.py, account.py.
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from django_module.apps.vpn.models import Client
from telegram_bot.handlers import static_text


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton(static_text.PERSONAL_ACCOUNT_BUTTON, callback_data=static_text.PERSONAL_ACCOUNT_CALLBACK)],
        [InlineKeyboardButton(static_text.INFO_BUTTON, callback_data=static_text.INFO_CALLBACK)]
    ]

    u, created = await Client.get_client_or_create(update.effective_user.to_dict())

    text = static_text.START_CREATED.format(first_name=u.username) if created \
        else static_text.START_OLD_USER.format(first_name=u.username)

    if context.user_data.get(static_text.START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    context.user_data[static_text.START_OVER] = False

    return static_text.CHOOSING_START
