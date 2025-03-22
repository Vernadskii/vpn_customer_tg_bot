import json
import os
from django.utils import timezone

from dateutil.relativedelta import relativedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import (
    ConversationHandler, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters,
)

import datetime as dt
from django_module.apps.vpn.models import Client, Subscription, PaymentHistory, Config
from logging_config import tgbot_logger
from telegram_bot.handlers import static_text
from telegram_bot.handlers.start_command import start_command
from telegram_bot.utils import notify_admin_users
from telegram_bot.vpn_service.service import VPNService, ConfigCreateError

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
    currency = "XTR"  # Используем Telegram Stars (XTR)
    price = price_dict[months_amount]  # Цена в XTR

    prices = [LabeledPrice(month_text, price)]

    await context.bot.send_invoice(
        chat_id=update.callback_query.message.chat.id,
        title=title,
        description=description,
        payload=json.dumps({"months_amount": months_amount}),
        provider_token="",  # Пустой токен для цифровых товаров
        currency=currency,
        prices=prices,
        start_parameter="start_parameter",
    )
    return static_text.BUYING_STATE


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


async def successful_payment_callback(update: Update, context: CallbackContext):
    payment = update.message.successful_payment
    months_amount = json.loads(payment.invoice_payload)['months_amount']
    client, _ = await Client.get_client_or_create(update.effective_user.to_dict())
    subscription = await Subscription.objects.acreate(
        client=client, start_date=dt.date.today(), end_date=dt.date.today()+relativedelta(months=months_amount),
        amount=months_amount,
    )
    await PaymentHistory.objects.acreate(
        payment_time=timezone.now(), transaction_id=payment.telegram_payment_charge_id,
        amount=payment.total_amount, subscription=subscription, invoice_payload=payment.invoice_payload,
    )
    try:
        config = await VPNService().create_config()
    except ConfigCreateError as ex:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f"Платеж успешно выполнен! В данный момент возникли технические сложности, "
                f"с вами свяжется специалист поддержки при первой возможности и вышлет конфиг."
            )
        )
        await notify_admin_users(
            context, f"Error ⚠️: Клиент {client.username} заплатил,"
                     f" но не получил конфиг так как VPN сервис оказался недоступен. Лог ошибки: {str(ex)}"
        )
        tgbot_logger.critical(f"Got ConfigCreateError after client payment: {str(ex)}")
        return

    config_file_path = await VPNService.create_file_by_config(config)
    await Config.objects.acreate(data=config.model_dump(exclude={"config_id"}), activated=True, vpn_id=config.config_id, subscription=subscription)
    await context.bot.send_document(
        update.effective_user.id,
        caption=f'Это ваш персональный файл конфигурации VPN. Он действует до {subscription.end_date}',
        document=config_file_path,
    )
    os.remove(config_file_path)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Спасибо за выбор!")
    tgbot_logger.info(f"Succesfully created new config {config.config_id} for user {client.username}")


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
