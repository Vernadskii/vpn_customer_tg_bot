from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

from telegram_bot.handlers import static_text


async def handle_account_selection(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()  # Подтверждаем, чтобы избежать "зависания"

    choice = query.data
    if choice == static_text.TOP_UP_ACCOUNT_CALLBACK:
        return await handle_top_up_balance(update, context)
    if choice == static_text.BUY_VPN_CALLBACK:
        return await handle_buy_subscription(update, context)
    if choice == static_text.MY_SUBSCRIPTIONS_CALLBACK:
        return await handle_my_subscription(update, context)
    # return await invalid_input(update, context)


async def handle_top_up_balance(update: Update, context: CallbackContext):
    await update.callback_query.message.reply_text(
        text="Здесь логика пополнения баланса",
    )
    return ConversationHandler.END


async def handle_buy_subscription(update: Update, context: CallbackContext):
    await update.callback_query.message.reply_text(
        text="Здесь логика приобретения подписки",
    )
    return ConversationHandler.END


async def handle_my_subscription(update: Update, context: CallbackContext):
    await update.callback_query.message.reply_text(
        text="Управление подпиской.",
    )
    return ConversationHandler.END