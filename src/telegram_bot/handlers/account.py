from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, CallbackContext, CallbackQueryHandler

from telegram_bot.handlers import static_text
from telegram_bot.handlers.start_command import start_command

simple_back_keyboard = [
    [
        InlineKeyboardButton(static_text.BACK, callback_data=static_text.BACK_ACCOUNT_CALLBACK),
    ],
]


async def propose_account(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [
            InlineKeyboardButton(static_text.TOP_UP_ACCOUNT_BUTTON, callback_data=static_text.TOP_UP_ACCOUNT_CALLBACK),
            InlineKeyboardButton(static_text.BUY_VPN_BUTTON, callback_data=static_text.BUY_VPN_CALLBACK)
        ],
        [
            InlineKeyboardButton(static_text.MY_SUBSCRIPTIONS_BUTTON,
                                 callback_data=static_text.MY_SUBSCRIPTIONS_CALLBACK)
        ],
        [
            InlineKeyboardButton(static_text.BACK, callback_data=static_text.BACK_CALLBACK),
        ]
    ]

    await update.callback_query.edit_message_text(
        text="Баланс: х\nДата окончания подписки: DD-MM-YYYY",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return static_text.CHOOSING_ACCOUNT_ACTION


async def handle_top_up_balance(update: Update, context: CallbackContext):
    await update.callback_query.edit_message_text(
        text="Здесь логика пополнения баланса",
        reply_markup=InlineKeyboardMarkup(simple_back_keyboard),
    )
    return static_text.BACK_TO_ACCOUNT


async def handle_buy_subscription(update: Update, context: CallbackContext):
    await update.callback_query.edit_message_text(
        text="Здесь логика приобретения подписки",
        reply_markup=InlineKeyboardMarkup(simple_back_keyboard),
    )
    return static_text.BACK_TO_ACCOUNT


async def handle_my_subscription(update: Update, context: CallbackContext):
    await update.callback_query.edit_message_text(
        text="Управление подпиской.",
        reply_markup=InlineKeyboardMarkup(simple_back_keyboard),
    )
    return static_text.BACK_TO_ACCOUNT


async def handle_end_account_level(update: Update, context: CallbackContext):
    """Возврат в меню /start."""
    context.user_data[static_text.START_OVER] = True
    await start_command(update, context)

    return ConversationHandler.END


async def handle_back_to_account(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    await propose_account(update, context)
    return static_text.CHOOSING_ACCOUNT_ACTION


async def stop_nested(update: Update, context: CallbackContext) -> str:
    """Completely end conversation from within nested conversation."""
    await update.message.reply_text(static_text.STOP_TEXT)

    return static_text.STOPPING


# Set up second level ConversationHandler (account)
account_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(propose_account, pattern=f"^{static_text.PERSONAL_ACCOUNT_CALLBACK}$")],
    states={
        static_text.CHOOSING_ACCOUNT_ACTION: [
            CallbackQueryHandler(handle_top_up_balance, pattern=f"^{static_text.TOP_UP_ACCOUNT_CALLBACK}$"),
            CallbackQueryHandler(handle_buy_subscription, pattern=f"^{static_text.BUY_VPN_CALLBACK}$"),
            CallbackQueryHandler(handle_my_subscription, pattern=f"^{static_text.MY_SUBSCRIPTIONS_CALLBACK}$"),
            CallbackQueryHandler(handle_end_account_level, pattern=f"^{static_text.BACK_CALLBACK}$"),
        ],
        static_text.BACK_TO_ACCOUNT: [
            CallbackQueryHandler(handle_back_to_account, pattern=f"^{static_text.BACK_ACCOUNT_CALLBACK}$")]
    },
    fallbacks=[
        CommandHandler("stop", stop_nested),
    ],
    map_to_parent={
        # Return to top level menu
        ConversationHandler.END: static_text.CHOOSING_START,
        # End conversation altogether
        static_text.STOPPING: ConversationHandler.END,  # redirect from /stop
    },
)
