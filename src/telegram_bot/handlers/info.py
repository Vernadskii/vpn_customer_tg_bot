from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler, CallbackContext, CallbackQueryHandler, CommandHandler
from telegram_bot.handlers import static_text
from telegram_bot.handlers.start_command import start_command

simple_back_keyboard = [
        [
            InlineKeyboardButton(static_text.BACK, callback_data=static_text.BACK_INFO_CALLBACK),
        ],
    ]


async def propose_info(update: Update, context: CallbackContext) -> int:
    info_keyboard = [
        [
            InlineKeyboardButton(static_text.ABOUT_US_BUTTON, callback_data=static_text.ABOUT_US_CALLBACK),
            InlineKeyboardButton(static_text.PRICING_BUTTON, callback_data=static_text.PRICING_CALLBACK),
        ],
        [
            InlineKeyboardButton(static_text.HOW_TO_USE_BUTTON, callback_data=static_text.HOW_TO_USE_CALLBACK),
            InlineKeyboardButton(static_text.SUPPORT_BUTTON, callback_data=static_text.SUPPORT_CALLBACK),
        ],
        [
            InlineKeyboardButton(static_text.BACK, callback_data=static_text.BACK_CALLBACK),
        ]
    ]

    await update.callback_query.edit_message_text(
        text="Выберите раздел:",
        reply_markup=InlineKeyboardMarkup(info_keyboard)
    )
    await update.callback_query.answer()

    return static_text.CHOOSING_INFO


async def handle_about_us(update: Update, context: CallbackContext):
    await update.callback_query.edit_message_text(
        text="Здесь информация о нас.",
        reply_markup=InlineKeyboardMarkup(simple_back_keyboard),
    )
    return static_text.BACK_TO_INFO


async def handle_price(update: Update, context: CallbackContext):
    await update.callback_query.edit_message_text(
        text="Здесь наш прейскурант",
        reply_markup=InlineKeyboardMarkup(simple_back_keyboard),
    )
    return static_text.BACK_TO_INFO


async def handle_instruction(update: Update, context: CallbackContext):
    await update.callback_query.edit_message_text(
        text="Здесь инструкция по использованию.",
        reply_markup=InlineKeyboardMarkup(simple_back_keyboard),
    )
    return static_text.BACK_TO_INFO


async def handle_support(update: Update, context: CallbackContext):
    await update.callback_query.edit_message_text(
        text="Здесь поддержка. Заглушка -- TODO",
        reply_markup=InlineKeyboardMarkup(simple_back_keyboard),
    )
    return static_text.BACK_TO_INFO


async def handle_end_info_level(update: Update, context: CallbackContext):
    """Возврат в меню /start."""
    context.user_data[static_text.START_OVER] = True
    await start_command(update, context)

    return ConversationHandler.END


async def handle_back_to_info(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    await propose_info(update, context)
    return static_text.CHOOSING_INFO


async def stop_nested(update: Update, context: CallbackContext) -> str:
    """Completely end conversation from within nested conversation."""
    await update.message.reply_text(static_text.STOP_TEXT)

    return static_text.STOPPING


# Set up second level ConversationHandler (info)
info_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(propose_info, pattern=f"^{static_text.INFO_CALLBACK}$")],
    states={
        static_text.CHOOSING_INFO: [
            CallbackQueryHandler(handle_about_us, pattern=f"^{static_text.ABOUT_US_CALLBACK}$"),
            CallbackQueryHandler(handle_price, pattern=f"^{static_text.PRICING_CALLBACK}$"),
            CallbackQueryHandler(handle_instruction, pattern=f"^{static_text.HOW_TO_USE_CALLBACK}$"),
            CallbackQueryHandler(handle_support, pattern=f"^{static_text.SUPPORT_CALLBACK}$"),
            CallbackQueryHandler(handle_end_info_level, pattern=f"^{static_text.BACK_CALLBACK}$"),
        ],
        static_text.BACK_TO_INFO: [CallbackQueryHandler(handle_back_to_info, pattern=f"^{static_text.BACK_INFO_CALLBACK}$")]
    },
    fallbacks=[
        CommandHandler("stop", stop_nested),
    ],
    map_to_parent={
        # Return to top level menu
        ConversationHandler.END: static_text.CHOOSING_START,
        # End conversation altogether
        static_text.STOPPING: ConversationHandler.END,
    },
)





