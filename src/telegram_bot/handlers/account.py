from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import ConversationHandler, CommandHandler, CallbackContext, CallbackQueryHandler, \
    PreCheckoutQueryHandler, MessageHandler, filters

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


async def handle_buy_subscription(update: Update, context: CallbackContext):
    price_tmp = "Период: {period}, цена: {price}"
    keyboard = [
        [
            InlineKeyboardButton(
                price_tmp.format(period=static_text.BUY_1_MONTH, price=static_text.PRICE_1_MONTH),
                callback_data=static_text.BUY_1_MONTH_CALLBACK,
            ),
        ],
        [
            InlineKeyboardButton(
                price_tmp.format(period=static_text.BUY_3_MONTH, price=static_text.PRICE_3_MONTH),
                callback_data=static_text.BUY_3_MONTH_CALLBACK,
            ),
        ],
        [
            InlineKeyboardButton(
                price_tmp.format(period=static_text.BUY_6_MONTH, price=static_text.PRICE_6_MONTH),
                callback_data=static_text.BUY_6_MONTH_CALLBACK,
            )
        ],
        [
            InlineKeyboardButton(static_text.BACK, callback_data=static_text.BACK_ACCOUNT_CALLBACK),
        ],
    ]
    await update.callback_query.edit_message_text(
        text="У нас есть следующие тарифные планы:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return static_text.CHOOSING_PRICE


async def handle_buy_specific(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    price_dict = {1: static_text.PRICE_1_MONTH, 3: static_text.PRICE_3_MONTH, 6: static_text.PRICE_6_MONTH}
    month_text_dict = {1: static_text.BUY_1_MONTH, 3: static_text.BUY_3_MONTH, 6: static_text.BUY_6_MONTH}
    months_amount = int(update.callback_query.data[0])
    assert months_amount in month_text_dict, f"{months_amount} not in {month_text_dict.keys()}"
    month_text = month_text_dict[int(months_amount)]
    title = f"Подписка VPN на {month_text}"
    description = "После оплаты этого счета вам будет присвоен конфиг для пользования ВПН-ом"
    payload = "Custom-Payload"
    currency = "XTR"  # Используем Telegram Stars (XTR)
    price = price_dict[months_amount]  # Цена в XTR

    prices = [LabeledPrice(month_text, price)]

    await context.bot.send_invoice(
        chat_id=update.callback_query.message.chat.id,
        title=title,
        description=description,
        payload=payload,
        provider_token="",  # Пустой токен для цифровых товаров
        currency=currency,
        prices=prices,
        start_parameter="start_parameter"
    )
    return static_text.BUYING_STATE


async def precheckout_callback(update: Update, context: CallbackContext):
    query = update.pre_checkout_query
    if query.invoice_payload != 'Custom-Payload':
        await query.answer(ok=False, error_message="Что-то пошло не так...")
    else:
        await query.answer(ok=True)


async def successful_payment_callback(update: Update, context: CallbackContext):
    payment = update.message.successful_payment
    telegram_payment_charge_id = payment.telegram_payment_charge_id
    await update.message.reply_text(f"Платеж успешно выполнен! Ваш ID: {telegram_payment_charge_id}")


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
            CallbackQueryHandler(handle_buy_subscription, pattern=f"^{static_text.BUY_VPN_CALLBACK}$"),
            CallbackQueryHandler(handle_my_subscription, pattern=f"^{static_text.MY_SUBSCRIPTIONS_CALLBACK}$"),
            CallbackQueryHandler(handle_end_account_level, pattern=f"^{static_text.BACK_CALLBACK}$"),
        ],
        static_text.BACK_TO_ACCOUNT: [
            CallbackQueryHandler(handle_back_to_account, pattern=f"^{static_text.BACK_ACCOUNT_CALLBACK}$"),
        ],
        static_text.CHOOSING_PRICE: [
            CallbackQueryHandler(handle_buy_specific, pattern=f"^{static_text.BUY_CALLBACK_PATTERN}$"),
            CallbackQueryHandler(handle_back_to_account, pattern=f"^{static_text.BACK_ACCOUNT_CALLBACK}$"),
        ],
        static_text.BUYING_STATE: [
            PreCheckoutQueryHandler(precheckout_callback),
            MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback)
        ]
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
