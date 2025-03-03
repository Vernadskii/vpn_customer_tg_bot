from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from telegram_bot.handlers import static_text


async def handle_info_selection(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()  # Подтверждаем, чтобы избежать "зависания"

    choice = query.data
    if choice == static_text.ABOUT_US_CALLBACK:
        return await handle_about_us(update, context)
    elif choice == static_text.PRICING_CALLBACK:
        return await handle_price(update, context)
    elif choice == static_text.HOW_TO_USE_CALLBACK:
        return await handle_instruction(update, context)
    elif choice == static_text.SUPPORT_CALLBACK:
        return await handle_support(update, context)


async def handle_about_us(update: Update, context: CallbackContext):
    await update.callback_query.message.reply_text(
        text="Здесь информация о нас.",
    )
    return ConversationHandler.END


async def handle_price(update: Update, context: CallbackContext):
    await update.callback_query.message.reply_text(
        text="Здесь наш прейскурант",
    )
    return ConversationHandler.END


async def handle_instruction(update: Update, context: CallbackContext):
    await update.callback_query.message.reply_text(text="Здесь инструкция по использованию.")
    return ConversationHandler.END


async def handle_support(update: Update, context: CallbackContext):
    await update.callback_query.message.reply_text(text="Здесь поддержка.")
    return ConversationHandler.END