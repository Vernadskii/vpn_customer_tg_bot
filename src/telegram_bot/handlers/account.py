from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

from django_module.apps.users.models import User
from telegram_bot.handlers import static_text


async def handle_top_up_balance(update: Update, context: CallbackContext):
    await update.message.reply_text(
        text="Здесь логика пополнения баланса",
    )
    return ConversationHandler.END


async def handle_buy_subscription(update: Update, context: CallbackContext):
    await update.message.reply_text(
        text="Здесь логика приобретения подписки",
    )
    return ConversationHandler.END


async def handle_my_subscription(update: Update, context: CallbackContext):
    await update.message.reply_text(
        text="Управление подпиской.",
    )
    return ConversationHandler.END