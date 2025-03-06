from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, CallbackContext

from telegram_bot.handlers import static_text
from telegram_bot.handlers.info import info_conversation
from telegram_bot.handlers.start_command import start_command


async def handle_account(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [
            InlineKeyboardButton(static_text.TOP_UP_ACCOUNT_BUTTON, callback_data=static_text.TOP_UP_ACCOUNT_CALLBACK),
            InlineKeyboardButton(static_text.BUY_VPN_BUTTON, callback_data=static_text.BUY_VPN_CALLBACK)
        ],
        [
            InlineKeyboardButton(static_text.MY_SUBSCRIPTIONS_BUTTON, callback_data=static_text.MY_SUBSCRIPTIONS_CALLBACK)
        ]
    ]

    await update.callback_query.message.reply_text(
        text="Баланс: х\nДата окончания подписки: DD-MM-YYYY",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return static_text.CHOOSING_ACCOUNT


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End Conversation by command."""
    await update.message.reply_text(static_text.STOP_TEXT)

    return ConversationHandler.END


start_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_command)],
    states={
        static_text.CHOOSING_START: [
            info_conversation,  # account_conversation,
        ],
    },
    fallbacks=[
        CommandHandler("stop", stop),
    ],
)
