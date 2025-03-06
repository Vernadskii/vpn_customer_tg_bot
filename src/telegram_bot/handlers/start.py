from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, CallbackContext

from telegram_bot.handlers import static_text
from telegram_bot.handlers.account import account_conversation
from telegram_bot.handlers.info import info_conversation
from telegram_bot.handlers.start_command import start_command


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End Conversation by command."""
    await update.message.reply_text(static_text.STOP_TEXT)

    return ConversationHandler.END


start_conversation = ConversationHandler(
    entry_points=[CommandHandler("start", start_command)],
    states={
        static_text.CHOOSING_START: [
            info_conversation,
            account_conversation,
        ],
    },
    fallbacks=[
        CommandHandler("stop", stop),
    ],
)
