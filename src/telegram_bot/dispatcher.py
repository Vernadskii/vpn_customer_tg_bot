"""Telegram event handlers."""
import json
import os

from dateutil.relativedelta import relativedelta
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import (
    Application, MessageHandler, PreCheckoutQueryHandler, CallbackContext, filters,
)
import datetime as dt
from django_module.apps.vpn.models import Subscription, Client, PaymentHistory, Config
from telegram_bot.handlers.start import start_conversation
from telegram_bot.vpn_service.service import VPNService


async def notify_admin_users(context: CallbackContext, message: str):
    admin_clients = await Client.get_admin_clients()
    # Iterate over the admin clients and send a message
    for client in admin_clients:
        try:
            await context.bot.send_message(chat_id=client.chat_id, text=message)
        except TelegramError as e:
            print(f"Failed to send message to {client.chat_id}: {e}")


async def precheckout_callback(update: Update, context: CallbackContext):
    query = update.pre_checkout_query
    if False:
        await query.answer(ok=False, error_message="Что-то пошло не так...")
    await query.answer(ok=True)


async def successful_payment_callback(update: Update, context: CallbackContext):
    payment = update.message.successful_payment
    months_amount = json.loads(payment.invoice_payload)['months_amount']
    client, _ = await Client.get_client_or_create(update, context)
    subscription = Subscription.objects.create(
        client=client, start_date=dt.date.today(), end_date=dt.date.today()+relativedelta(month=months_amount),
        amount=months_amount,
    )
    PaymentHistory.objects.create(
        client=client, payment_date=dt.datetime.now(), transaction_id=payment.telegram_payment_charge_id,
        amount=payment.total_amount
    )
    config = await VPNService().create_config()
    if config is None:
        await update.message.reply_text(
            f"Платеж успешно выполнен! В данный момент возникли технические сложности, "
            f"с вами свяжется специалист поддержки при первой возможности"
        )
        await notify_admin_users(
            context, f"Клиент {client.username} заплатил, но не получил конфиг так как VPN сервис оказался недоступен."
        )
        return

    config_file_path = await VPNService.create_file_by_config(config)
    Config.objects.create(data=config.model_dump(), activated=True, vpn_id=config.config_id, subscription=subscription)
    await context.bot.send_document(
        update.effective_user.id,
        caption=f'Это ваш персональный файл конфигурации VPN. Он действует до {subscription.end_date}',
        document=config_file_path,
    )
    os.remove(config_file_path)
    await update.message.reply_text(f"Спасибо за выбор!")


def setup_handlers(app: Application):
    """Adding handlers for events from Telegram."""

    # onboarding
    app.add_handler(start_conversation)
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback),)